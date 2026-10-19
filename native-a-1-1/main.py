"""나만의 프롬프트 관리 프로그램 (콘솔)

프롬프트는 prompts.json 파일에 저장되어 프로그램을 종료해도 유지된다.
"""

import json
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# 테스트나 다른 위치 사용을 위해 환경변수로 저장 위치를 바꿀 수 있다.
DATA_FILE = Path(os.environ.get("PROMPT_DATA_FILE", BASE_DIR / "prompts.json"))
EXPORT_DIR = Path(os.environ.get("PROMPT_EXPORT_DIR", BASE_DIR / "exports"))

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

# 이전 미션(멀티모달 콘텐츠 제작 — Lumin 광고 영상)에서 직접 작성한 프롬프트
# 출처: gen-ai-basic-2 저장소 docs/04_prompts.md (실제 생성에 성공한 씬 1·3·5 + BGM)
DEFAULT_PROMPTS = [
    {
        "title": "Lumin 광고 씬1 — 퇴근 직후 거실 키비주얼",
        "content": (
            "A cluttered living room right after someone came home from work, "
            "a coat and bag left near the door, shoes kicked off, cold white fluorescent light, "
            "evening blue-toned atmosphere outside the window, warm amber tone accent, "
            "cinematic lighting, 35mm lens, shallow depth of field, "
            "minimal Korean apartment interior, empty room, no people"
        ),
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "Lumin 광고 씬1 — 퇴근 직후 거실 모션 (Veo)",
        "content": (
            "A cluttered living room right after someone came home from work, "
            "a coat and bag left near the door, shoes kicked off, cold white fluorescent light, "
            "evening blue-toned atmosphere outside the window, cinematic lighting, 35mm lens, "
            "shallow depth of field, minimal Korean apartment interior, empty room, no people. "
            "Slow subtle push-in camera movement, very slight ambient dust particles in the cold light, "
            "8 seconds, no camera shake"
        ),
        "category": "영상 생성",
        "favorite": True,
    },
    {
        "title": "Lumin 광고 씬3 — 조명 전환 키비주얼",
        "content": (
            "Wide shot of a living room where cold white light is transforming into warm amber light, "
            "soft scent smoke/particles diffusing gently in the air, visible light gradient across the room, "
            "cinematic lighting, 35mm lens, shallow depth of field, minimal Korean apartment interior, "
            "warm amber tone, keep same style as previous images, no visible face"
        ),
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "Lumin 광고 씬3 — 빛과 향의 변화 모션 (Veo)",
        "content": (
            "Wide shot of a living room where cold white light is transforming into warm amber light, "
            "soft scent smoke/particles diffusing gently in the air, cinematic lighting, 35mm lens, "
            "shallow depth of field, minimal Korean apartment interior, no visible face. "
            "Smooth transition of light color temperature from cool white to warm amber across 8 seconds, "
            "scent particles slowly drifting and diffusing in the light beam, gentle camera drift"
        ),
        "category": "영상 생성",
        "favorite": True,
    },
    {
        "title": "Lumin 광고 씬5 — 제품 실루엣 아웃트로",
        "content": (
            "Dark minimal background with the Lumin device silhouette glowing warm amber light in the center, "
            "soft bokeh light particles, cinematic product photography style, 35mm lens, "
            "shallow depth of field, warm amber tone, consistent with previous scenes, "
            "empty negative space on the right side for text overlay"
        ),
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "Lumin 광고 씬5 — 제품 페이드인 모션 (Veo)",
        "content": (
            "Dark minimal background with a smart mood-light and scent diffuser device silhouette "
            "glowing warm amber light in the center, soft bokeh light particles, "
            "cinematic product photography style, 35mm lens, shallow depth of field, warm amber tone. "
            "Slow fade-in of the glowing device from darkness, gentle light pulse, 8 seconds, static camera"
        ),
        "category": "영상 생성",
        "favorite": False,
    },
    {
        "title": "Lumin 광고 BGM (38초 로파이)",
        "content": (
            "Lo-fi ambient track, warm and calming, soft piano and gentle synth pad, "
            "slow tempo (around 70 BPM), evening relaxation mood, minimal percussion, "
            "no vocals, 38 seconds"
        ),
        "category": "기타",
        "favorite": False,
    },
]

MENU_ITEMS = [
    ("1", "프롬프트 추가"),
    ("2", "프롬프트 목록"),
    ("3", "카테고리별 조회"),
    ("4", "프롬프트 검색"),
    ("5", "프롬프트 상세 보기"),
    ("6", "즐겨찾기 관리"),
    ("7", "즐겨찾기 목록"),
    ("8", "Markdown 내보내기"),
    ("0", "종료"),
]


def input_non_empty(message):
    """빈 값이 아닐 때까지 반복해서 입력받는다."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("입력값이 비어 있습니다. 다시 입력해주세요.")


def input_number(message, min_value, max_value):
    """min_value~max_value 범위의 정수를 입력받는다. 잘못된 입력이면 None을 반환한다."""
    value = input(message).strip()
    try:
        number = int(value)
    except ValueError:
        print("숫자를 입력해주세요.")
        return None
    if number < min_value or number > max_value:
        print(f"{min_value}~{max_value} 사이의 번호를 입력해주세요.")
        return None
    return number


def choose_category():
    """미리 정의된 카테고리 중 하나를 고르거나 직접 입력받는다."""
    custom_number = len(CATEGORIES) + 1
    while True:
        print("카테고리 선택:")
        for number, category in enumerate(CATEGORIES, start=1):
            print(f"{number}) {category}")
        print(f"{custom_number}) 직접 입력")

        number = input_number("선택: ", 1, custom_number)
        if number is None:
            continue
        if number == custom_number:
            return input_non_empty("카테고리 이름: ")
        return CATEGORIES[number - 1]


def add_prompt(prompts):
    """새 프롬프트를 입력받아 목록에 추가한다."""
    print("\n=== 프롬프트 추가 ===")
    title = input_non_empty("제목: ")
    content = input_non_empty("내용: ")
    print()
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
    })
    print("\n프롬프트가 추가되었습니다!")


def print_prompt_line(number, prompt):
    """'번호. [카테고리] 제목 ⭐' 형식으로 한 줄 출력한다."""
    star = " ⭐" if prompt["favorite"] else ""
    print(f"{number}. [{prompt['category']}] {prompt['title']}{star}")


def show_list(prompts):
    """저장된 모든 프롬프트를 번호와 함께 출력한다."""
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다. 먼저 프롬프트를 추가해주세요.")
        return

    for number, prompt in enumerate(prompts, start=1):
        print_prompt_line(number, prompt)
    print(f"\n총 {len(prompts)}개의 프롬프트")


def find_prompts(prompts, condition):
    """condition(prompt)가 참인 프롬프트를 (전체 목록 기준 번호, 프롬프트) 목록으로 반환한다.

    전체 목록 기준 번호를 유지해서, 결과에 보이는 번호를
    상세 보기/즐겨찾기 관리에 그대로 입력할 수 있게 한다.
    """
    return [
        (number, prompt)
        for number, prompt in enumerate(prompts, start=1)
        if condition(prompt)
    ]


def print_matches(matches):
    """find_prompts()의 결과를 출력한다."""
    for number, prompt in matches:
        print_prompt_line(number, prompt)


def get_all_categories(prompts):
    """기본 카테고리에 사용자가 직접 입력한 카테고리를 더한 목록을 반환한다."""
    categories = list(CATEGORIES)
    for prompt in prompts:
        if prompt["category"] not in categories:
            categories.append(prompt["category"])
    return categories


def show_by_category(prompts):
    """선택한 카테고리의 프롬프트만 출력한다."""
    print("\n=== 카테고리별 조회 ===")
    categories = get_all_categories(prompts)
    for number, category in enumerate(categories, start=1):
        print(f"{number}) {category}")

    number = input_number("선택: ", 1, len(categories))
    if number is None:
        return
    category = categories[number - 1]

    matches = find_prompts(prompts, lambda prompt: prompt["category"] == category)
    print(f"\n[{category}] 카테고리 프롬프트:")
    if not matches:
        print("이 카테고리에 등록된 프롬프트가 없습니다.")
        return
    print_matches(matches)
    print(f"\n총 {len(matches)}개의 프롬프트")


def search_prompt(prompts):
    """키워드가 제목 또는 내용에 포함된 프롬프트를 찾는다 (대소문자 무시)."""
    print("\n=== 프롬프트 검색 ===")
    keyword = input_non_empty("검색어: ").lower()

    matches = find_prompts(
        prompts,
        lambda prompt: keyword in prompt["title"].lower()
        or keyword in prompt["content"].lower(),
    )
    print("\n검색 결과:")
    if not matches:
        print("검색 결과가 없습니다.")
        return
    print_matches(matches)
    print(f"\n{len(matches)}개의 프롬프트를 찾았습니다.")


def select_prompt(prompts):
    """번호를 입력받아 해당 프롬프트를 반환한다. 잘못된 번호면 None."""
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return None
    number = input_number(f"번호 입력 (1~{len(prompts)}): ", 1, len(prompts))
    if number is None:
        return None
    return prompts[number - 1]


def show_detail(prompts):
    """선택한 프롬프트의 전체 내용을 출력한다."""
    print("\n=== 프롬프트 상세 보기 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    line = "─" * 40
    print()
    print(line)
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '-'}")
    print(line)
    print("내용:")
    print(prompt["content"])
    print(line)


def toggle_favorite(prompts):
    """선택한 프롬프트의 즐겨찾기 상태를 추가/해제한다."""
    print("\n=== 즐겨찾기 관리 ===")
    prompt = select_prompt(prompts)
    if prompt is None:
        return

    prompt["favorite"] = not prompt["favorite"]
    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다! ⭐")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다.")


def show_favorites(prompts):
    """즐겨찾기된 프롬프트만 모아서 출력한다."""
    print("\n=== 즐겨찾기 목록 ===")
    matches = find_prompts(prompts, lambda prompt: prompt["favorite"])
    if not matches:
        print("즐겨찾기한 프롬프트가 없습니다. (메뉴 6번에서 추가할 수 있습니다)")
        return
    print_matches(matches)
    print(f"\n총 {len(matches)}개의 즐겨찾기")


def default_prompts():
    """기본 프롬프트를 복사해서 반환한다 (원본 DEFAULT_PROMPTS 보호)."""
    return [dict(prompt) for prompt in DEFAULT_PROMPTS]


def normalize_prompt(raw):
    """파일에서 읽은 항목을 프롬프트 딕셔너리로 정리한다. 필수 필드가 없으면 ValueError."""
    if not isinstance(raw, dict):
        raise ValueError("프롬프트 항목이 딕셔너리가 아닙니다.")
    for field in ("title", "content", "category"):
        if not isinstance(raw.get(field), str) or not raw[field].strip():
            raise ValueError(f"'{field}' 필드가 없거나 비어 있습니다.")
    return {
        "title": raw["title"],
        "content": raw["content"],
        "category": raw["category"],
        "favorite": bool(raw.get("favorite", False)),
    }


def load_prompts(path=DATA_FILE):
    """JSON 파일에서 프롬프트를 불러온다.

    파일이 없으면 기본 데이터를 쓰고, 파일이 손상됐으면 .bak으로 옮겨 두고 기본 데이터를 쓴다.
    """
    if not path.exists():
        return default_prompts()
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("최상위 값이 리스트가 아닙니다.")
        return [normalize_prompt(item) for item in data]
    except (OSError, ValueError) as error:  # JSONDecodeError는 ValueError의 하위 클래스
        backup = path.with_suffix(path.suffix + ".bak")
        print(f"저장 파일을 읽을 수 없어 기본 데이터로 시작합니다. ({error})")
        try:
            path.replace(backup)
            print(f"손상된 파일은 {backup.name}로 옮겨 두었습니다.")
        except OSError:
            pass
        return default_prompts()


def save_prompts(prompts, path=DATA_FILE):
    """프롬프트를 JSON 파일로 저장한다. 임시 파일에 먼저 쓴 뒤 교체해서 저장 중 손상을 막는다."""
    temp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(prompts, file, ensure_ascii=False, indent=2)
        temp_path.replace(path)
    except OSError as error:
        print(f"저장에 실패했습니다: {error}")


def safe_filename(name):
    """카테고리 이름을 파일 이름으로 쓸 수 있게 정리한다."""
    return re.sub(r'[\\/:*?"<>|\s]+', "_", name).strip("_") or "category"


def export_markdown(prompts):
    """카테고리별로 Markdown 파일(exports/<카테고리>.md)을 만든다."""
    print("\n=== Markdown 내보내기 ===")
    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    for category in get_all_categories(prompts):
        items = [prompt for prompt in prompts if prompt["category"] == category]
        if not items:
            continue
        lines = [f"# {category}", ""]
        for prompt in items:
            star = " ⭐" if prompt["favorite"] else ""
            lines += [f"## {prompt['title']}{star}", "", "```text", prompt["content"], "```", ""]
        path = EXPORT_DIR / f"{safe_filename(category)}.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"- {path.name} ({len(items)}개)")
    print(f"\n{EXPORT_DIR} 폴더에 저장했습니다.")


def show_menu():
    """메인 메뉴를 출력한다."""
    print()
    print("=== 나만의 프롬프트 관리 ===")
    for key, label in MENU_ITEMS:
        print(f"{key}. {label}")


def main():
    prompts = load_prompts()

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            add_prompt(prompts)
            save_prompts(prompts)
        elif choice == "2":
            show_list(prompts)
        elif choice == "3":
            show_by_category(prompts)
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "5":
            show_detail(prompts)
        elif choice == "6":
            toggle_favorite(prompts)
            save_prompts(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "8":
            export_markdown(prompts)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 메뉴 번호(0~8)를 입력해주세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
