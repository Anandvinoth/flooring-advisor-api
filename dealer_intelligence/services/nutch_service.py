import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse


class NutchService:
    CONTAINER_NAME = "apache_nutch"
    NUTCH_HOME = "/root/nutch_source/runtime/local"

    def __init__(self, site_id: str, dealer_url: str):
        self.site_id = site_id
        self.dealer_url = dealer_url.rstrip("/")

        hostname = urlparse(self.dealer_url).hostname or ""
        self.domain = hostname.removeprefix("www.")

        self.host_root = Path("data") / "nutch" / site_id
        self.host_seed_dir = self.host_root / "seed"
        self.host_filter_file = self.host_root / "regex-urlfilter.txt"

        self.container_root = f"/root/nutch/{site_id}"
        self.container_seed_dir = f"{self.container_root}/seed"
        self.container_output_dir = f"{self.container_root}/output"
        self.container_filter_file = (
            f"{self.container_root}/regex-urlfilter.txt"
        )

    def prepare_filter(self) -> Path:
        escaped_domain = re.escape(self.domain)

        rules = f"""# Block assets
-(?i).*\\.(svg|jpg|jpeg|png|gif|webp|ico|css|js|woff|woff2|ttf|eot|mp4|mp3)(\\?.*)?$

# Allow current dealer domain only
+^https?://([a-z0-9-]+\\.)?{escaped_domain}(/.*)?$

# Reject everything else
-.
"""

        self.host_root.mkdir(parents=True, exist_ok=True)
        self.host_filter_file.write_text(rules, encoding="utf-8")

        return self.host_filter_file

    def copy_inputs(self) -> None:
        container_conf_dir = f"{self.container_root}/conf"

        subprocess.run(
            [
                "docker",
                "exec",
                self.CONTAINER_NAME,
                "sh",
                "-lc",
                (
                    f"mkdir -p {self.container_seed_dir} {container_conf_dir} && "
                    f"cp -R {self.NUTCH_HOME}/conf/. {container_conf_dir}/ && "
                    f"rm -rf {self.container_output_dir}"
                ),
            ],
            check=True,
        )

        subprocess.run(
            [
                "docker",
                "cp",
                str(self.host_seed_dir / "urls"),
                f"{self.CONTAINER_NAME}:{self.container_seed_dir}/urls",
            ],
            check=True,
        )

        subprocess.run(
            [
                "docker",
                "cp",
                str(self.host_filter_file),
                (
                    f"{self.CONTAINER_NAME}:"
                    f"{container_conf_dir}/regex-urlfilter.txt"
                ),
            ],
            check=True,
        )

    def crawl(self, rounds: int = 2) -> None:
        container_conf_dir = f"{self.container_root}/conf"

        subprocess.run(
            [
                "docker",
                "exec",
                self.CONTAINER_NAME,
                "rm",
                "-rf",
                self.container_output_dir,
            ],
            check=True,
        )

        command = [
            "docker",
            "exec",
            "-e",
            f"NUTCH_CONF_DIR={container_conf_dir}",
            self.CONTAINER_NAME,
            f"{self.NUTCH_HOME}/bin/crawl",
            "-s",
            self.container_seed_dir,
            self.container_output_dir,
            str(rounds),
        ]

        subprocess.run(command, check=True)

    def index(self) -> None:
        command = [
            "docker",
            "exec",
            self.CONTAINER_NAME,
            "bash",
            "-lc",
            (
                f"{self.NUTCH_HOME}/bin/nutch index "
                f"{self.container_output_dir}/crawldb "
                f"-linkdb {self.container_output_dir}/linkdb "
                f"{self.container_output_dir}/segments/*"
            ),
        ]

        subprocess.run(command, check=True)