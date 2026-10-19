"""나만의 프롬프트 관리 프로그램 (콘솔)."""

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

# 프로그램 실행 중에만 유지되는 데이터 (종료하면 초기화)
prompts = [
    {
        "title": "블로그 글 작성 도우미",
        "content": (
            "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 SEO에 최적화된 "
            "블로그 글을 작성해주세요. 서론, 본론, 결론 구조를 갖추고, "
            "독자의 관심을 끄는 제목을 3개 제안해주세요."
        ),
        "category": "텍스트 생성",
        "favorite": False,
    },
    {
        "title": "제품 썸네일 생성",
        "content": (
            "다음 제품의 매력적인 썸네일 이미지를 생성해주세요. 밝은 스튜디오 조명, "
            "깔끔한 단색 배경, 제품이 화면 중앙에 오는 구도, 16:9 비율."
        ),
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "IT 컨설턴트 페르소나",
        "content": (
            "당신은 15년 경력의 IT 컨설턴트입니다. 비전문가도 이해할 수 있는 쉬운 말로 "
            "설명하고, 항상 장점과 단점을 함께 제시하며, 마지막에 다음 행동 제안을 "
            "한 줄로 정리해주세요."
        ),
        "category": "페르소나",
        "favorite": False,
    },
    {
        "title": "뉴스 요약 프롬프트",
        "content": (
            "아래 뉴스 기사를 핵심 3줄로 요약하고, 주요 키워드 5개와 "
            "기사의 논조(긍정/중립/부정)를 함께 알려주세요."
        ),
        "category": "자동화",
        "favorite": False,
    },
    {
        "title": "광고 스크립트 작성",
        "content": (
            "15초 분량의 제품 광고 영상 스크립트를 작성해주세요. 첫 3초 안에 시선을 끄는 "
            "장면, 핵심 혜택 한 가지, 마지막 행동 유도 문구를 포함해주세요."
        ),
        "category": "영상 생성",
        "favorite": False,
    },
]


def show_menu():
    """메인 메뉴를 출력한다."""
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")


def input_nonempty(label):
    """빈 값이 아닐 때까지 다시 입력받는다."""
    while True:
        value = input(label).strip()
        if value:
            return value
        print("입력값이 비어 있습니다. 다시 입력해주세요.")


def input_number(label, max_n):
    """1~max_n 범위의 번호를 입력받는다. 잘못된 입력이면 None을 반환한다."""
    value = input(label).strip()
    if not value.isdigit() or not 1 <= int(value) <= max_n:
        print(f"1~{max_n} 사이의 번호를 입력해주세요.")
        return None
    return int(value)


def choose_category():
    """카테고리를 목록에서 고르거나 직접 입력받는다."""
    print("\n카테고리 선택:")
    for i, name in enumerate(CATEGORIES, start=1):
        print(f"{i}) {name}")
    print("직접 입력하려면 카테고리 이름을 그대로 입력하세요.")
    while True:
        value = input("선택: ").strip()
        if value.isdigit() and 1 <= int(value) <= len(CATEGORIES):
            return CATEGORIES[int(value) - 1]
        if value and not value.isdigit():
            return value
        print("올바른 번호나 카테고리 이름을 입력해주세요.")


def add_prompt():
    """새 프롬프트를 등록한다. 즐겨찾기 기본값은 False."""
    print("\n=== 프롬프트 추가 ===")
    title = input_nonempty("제목: ")
    content = input_nonempty("내용: ")
    category = choose_category()
    prompts.append(
        {"title": title, "content": content, "category": category, "favorite": False}
    )
    print("\n프롬프트가 추가되었습니다!")


def format_line(number, prompt):
    """목록 한 줄: '1. [카테고리] 제목 ⭐'"""
    star = " ⭐" if prompt["favorite"] else ""
    return f"{number}. [{prompt['category']}] {prompt['title']}{star}"


def print_prompts(items):
    """(원래 번호, 프롬프트) 쌍의 목록을 출력한다."""
    for number, prompt in items:
        print(format_line(number, prompt))


def show_list():
    """저장된 모든 프롬프트를 번호와 함께 출력한다."""
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
    print_prompts(list(enumerate(prompts, start=1)))
    print(f"\n총 {len(prompts)}개의 프롬프트")


def main():
    """메뉴를 반복해서 보여주고 선택한 기능을 실행한다."""
    actions = {
        "1": add_prompt,
        "2": show_list,
    }
    while True:
        show_menu()
        choice = input("선택: ").strip()
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        action = actions.get(choice)
        if action is None:
            print("잘못된 입력입니다. 메뉴에 있는 번호를 입력해주세요.")
            continue
        action()


if __name__ == "__main__":
    main()
