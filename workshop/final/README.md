# Workshop Final

핸즈온 최종 완성본입니다. 모든 시나리오가 등록되어 있으며, 참석자 코드가 막혔을 때 비교용 정답 코드로 사용할 수 있습니다.

## 실행

```bash
uv sync
bash run.sh --scenario translate --topic "Gemma 4 is a family of models released by Google DeepMind." --tasks 10
```

주요 완성 흐름:

```bash
bash run.sh --scenario resume --topic "도서 출판사 소설 기획자" --tasks 10
bash run.sh --scenario interview_review --topic "도서 출판사 소설 기획자" --tasks 10
bash run.sh --scenario hiring_decision --topic "도서 출판사 소설 기획자" --hires 2

bash run.sh --scenario short_story_writing --topic "문예지 신인상 투고용 도시 미스터리 단편" --tasks 10
bash run.sh --scenario story_review_selection --topic "문예지 신인상 투고용 도시 미스터리 단편" --select 3 --tasks 3
bash run.sh --scenario story_revision --select 3 --tasks 3
bash run.sh --scenario publication_offer_email --select 3 --tasks 3
```

Windows PowerShell에서는 `bash run.sh` 대신 `.\run.ps1`을 사용합니다.
