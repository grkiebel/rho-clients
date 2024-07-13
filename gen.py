from rho_clients.generator.generate import Generator


def main():
    generator = Generator(source="http://localhost:8080/openapi.json")
    generator.run()
    generator.diagnostic()


if __name__ == "__main__":
    main()
    print("Done")
