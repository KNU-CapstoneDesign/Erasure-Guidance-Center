import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '설치된 패키지의 라이선스 목록을 가져옵니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-file',
            type=str,
            help='라이선스 목록을 저장할 파일 경로',
        )

    def handle(self, *args, **options):
        output_file = options.get('output_file')
        try:
            result = subprocess.run(
                ["pip-licenses", "--format=json"],
                capture_output=True,
                text=True,
                check=True
            )
            licenses = result.stdout
            if output_file:
                with open(output_file, "w") as f:
                    f.write(licenses)
                self.stdout.write(self.style.SUCCESS(
                    f"라이선스 목록이 {output_file}에 저장되었습니다."))
            else:
                self.stdout.write(licenses)
        except subprocess.CalledProcessError as e:
            self.stderr.write(f"오류 발생: {e}")
