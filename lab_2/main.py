import subprocess


def main():
    path = "src/gen/execute/gen_cpp.exe"
    output = subprocess.run(path, capture_output=True, text=True)
    print(output.stdout)

if __name__ == "__main__":
    main()