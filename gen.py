from rho_clients.generator.generate import Generator


def main():
    Generator().run(source="http://localhost:8080/openapi.json")


if __name__ == "__main__":
    main()
    print("Done")
