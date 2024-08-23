from rho_clients.client_apps import tool_mgr_d as tool_mgr


def main():
    tool_mgr.main(service_url="http://localhost:8080")


if __name__ == "__main__":
    main()
    print("Done")
