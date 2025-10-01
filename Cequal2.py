import sys

def run_c2_code(code: str):
    lines = code.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("print "):
            # print のあとに書かれた文字列を表示
            text = line[6:].strip()
            if text.startswith('"') and text.endswith('"'):
                print(text[1:-1])
            else:
                print(text)

def main():
    if len(sys.argv) < 2:
        print("使い方: py Cequal2.py <ファイル名.c2>")
        return
    
    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
        run_c2_code(code)
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {filename}")

if __name__ == "__main__":
    main()
