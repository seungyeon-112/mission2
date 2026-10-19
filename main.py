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


def main():
    """메뉴를 반복해서 보여주고 선택한 기능을 실행한다."""
    actions = {
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
