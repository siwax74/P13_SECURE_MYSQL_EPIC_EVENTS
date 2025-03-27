from controllers.init_controller import CLIController


def main():
    controller = CLIController()
    controller.run()
    return controller


if __name__ == "__main__":
    main()
