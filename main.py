from app.controllers.login_controller import LoginController


def main():
    controller = LoginController()
    controller.run()
    return controller


if __name__ == "__main__":
    main()
