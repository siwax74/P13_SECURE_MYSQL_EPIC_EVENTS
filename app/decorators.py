import time


def with_banner(func):
    def wrapper(self, *args, **kwargs):
        self.cli_view.print_banner()
        return func(self, *args, **kwargs)

    return wrapper


def safe_execution(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Erreur : {e}")
            time.sleep(1)

    return wrapper
