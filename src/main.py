import command

def main() -> int:
    try:
        command.execute()
    except Exception as error:
        print("Error occured: " + str(error))
        return 1
    return 0

if __name__ == "__main__":
    main()
