# GitHub 업로드 · GitHub Pages 실행 안내

이 안내는 패키지를 새 프로젝트 저장소에 올리는 방법입니다. 이미 업로드나 웹 배포가 완료되었다는 뜻은 아닙니다. GitHub 계정·저장소 이름은 사용자가 정하며, 아래 `YOUR_GITHUB_ID`는 바꿔 넣을 예시입니다.

## 1. 압축 풀기

ZIP을 풀면 `samguk-dodgeball` 폴더가 나옵니다. 이 폴더 안에서 `index.html`, `README.md`, `docs`, `data`, `assets` 등을 확인하세요.

**올리는 대상은 ZIP 파일이 아니라 압축을 푼 폴더의 내용입니다.**

올바른 저장소 첫 화면:

```text
index.html
README.md
.nojekyll
docs/
data/
assets/
tools/
...
```

잘못 넣은 예:

```text
samguk-dodgeball/index.html    ← 저장소 안에 바깥 폴더를 한 단계 더 넣음
samguk_dodgeball_github_v9.zip ← 압축만 올림
```

`main`의 `/(root)` 배포에서는 진입 파일이 그 루트에 있어야 합니다.[1]

## 2. 저장소 만들고 파일 올리기

GitHub에서 **New repository**를 엽니다. 저장소 이름은 `samguk-dodgeball`을 예로 사용할 수 있습니다. 무료 개인 계정의 Pages 배포는 **Public** 저장소를 사용합니다.[1]

빈 저장소라면 `uploading an existing file` 안내로, 이미 파일이 있는 저장소라면 **Add file → Upload files**로 업로드 화면을 엽니다. 압축을 푼 폴더의 내부 파일과 `assets`, `docs`, `data`, `tools` 하위 폴더를 올립니다.[2]

`Add samguk dodgeball v9`처럼 변경 설명을 적고 커밋합니다. 화면에 **Propose changes**가 나오는 방식으로 새 브랜치에 올렸다면, 해당 변경을 `main`에 병합한 뒤 다음 단계로 진행합니다. 저장소가 조직 관리 정책으로 보호되어 있으면 그 정책을 따르세요.[2]

점으로 시작하는 `.nojekyll`, `.gitignore`, `.gitattributes`도 포함합니다. 숨김 파일이 업로드되지 않았으면 **Add file → Create new file**로 추가할 수 있습니다. `.nojekyll`은 루트에 두는 정적 배포 표시 파일입니다.[1]

GitHub 웹 업로드는 한 번에 최대 100개 파일, 파일당 25 MiB까지 지원합니다. 이 패키지의 파일은 그 범위 안에 들어가도록 구성했습니다.[2]

## 3. Pages 켜기

저장소의 **Settings → Pages**로 들어갑니다. 다음 값으로 저장하세요.[3]

| 항목 | 선택 |
|---|---|
| Build and deployment → Source | **Deploy from a branch** |
| Branch | **main** |
| Folder | **/(root)** |
| 저장 버튼 | **Save** |

이 패키지에는 사용자 정의 Actions YAML 파일이 없습니다. **Source를 `GitHub Actions`로 바꾸지 않고 위 설정으로 배포**합니다. GitHub 자체 배포 작업은 Actions 화면에 표시될 수 있습니다.[3]

`main`이 보이지 않으면 먼저 파일을 `main`에 커밋했는지 확인합니다. 기존 저장소의 기본 브랜치가 다른 이름이면 실제로 `index.html`을 넣은 브랜치를 선택합니다.[3]

`/docs`를 배포 폴더로 고르면 안 됩니다. 이 패키지의 `docs`는 게임 진입 폴더가 아니라 설명서 폴더입니다.

## 4. 실제 게임 주소 확인

배포가 성공하면 **Settings → Pages → Visit site**로 엽니다. 저장소의 코드 보기 주소가 아니라 이 사이트 주소를 공유하면 됩니다.[1]

일반 프로젝트 Pages 주소의 형식:

```text
https://YOUR_GITHUB_ID.github.io/samguk-dodgeball/
```

사용자/조직 사이트는 구조가 다르므로 최종 주소는 항상 **Visit site**에 표시된 값을 기준으로 합니다.[4]

## 5. 기존 기록 옮기기

기존 v9 HTML에서 **기록 → 기록 파일 내보내기**를 누르거나 점령전 지도에서 **기록 저장**을 누릅니다. 배포한 사이트를 열고 **기록 → 기록 파일 불러오기**에서 같은 JSON을 선택합니다.

`localStorage`는 접속 출처별로 다르고 `file:` 주소의 저장 동작은 브라우저마다 다를 수 있습니다. 따라서 로컬 파일·다른 사이트·다른 기기 사이의 기록은 파일로 옮겨야 합니다.[5]

**개인 저장 JSON을 공개 저장소에 올릴 필요는 없습니다.** 게임 안에서 불러오기만 하세요. 새 기기에서 자동 동기화되는 서버 저장은 이 패키지에 없습니다.

## 6. 업데이트

새 HTML을 `index.html`이라는 이름으로 교체한 뒤 같은 배포 브랜치에 커밋합니다. 설명서와 참고 데이터가 바뀐 경우 해당 파일도 함께 교체합니다. 설정한 브랜치·폴더의 변경이 사이트에 반영됩니다.[3]

개인 기록을 백업한 뒤 업데이트하세요. 기록이 보이지 않는다는 이유로 브라우저 저장 데이터를 먼저 지우지 마세요.

## 문제가 생겼을 때

| 증상 | 먼저 확인할 것 |
|---|---|
| 404 또는 README만 표시 | `index.html` 철자·소문자·루트 위치, Pages의 브랜치·폴더.[1][6] |
| 배포 자체가 실패 | 저장소 Actions의 Pages 배포 작업과 오류 메시지.[3] |
| 변경한 화면이 안 나옴 | 교체한 파일이 `main/index.html`인지, 해당 커밋 배포가 성공했는지 확인한 뒤 새로고침. |
| 기존 군공·점령전이 안 보임 | 이전 파일에서 내보낸 기록 JSON을 게임 안에서 불러오기.[5] |
| 음악·효과음이 안 남 | 게임의 소리 버튼을 켜고 출전 버튼을 직접 눌러 보기. |
| 모바일에서 화면이 좁음 | 기기를 가로로 돌리고 게임의 전체 화면 기능을 사용. |

## Git 명령으로 올리는 경우 — 선택 사항

이미 Git을 사용하는 사람만 이 절을 사용하면 됩니다. **새 빈 저장소**를 만들고, 압축을 푼 `samguk-dodgeball` 폴더에서 실행합니다. 기존 저장소의 변경을 덮어쓰거나 강제 푸시하지 마세요.

```bash
git init
git add .
git commit -m "Package Samguk Dodgeball Atlas v9 for GitHub Pages"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_ID/samguk-dodgeball.git
git push -u origin main
```

`YOUR_GITHUB_ID`와 저장소 이름을 실제 값으로 변경하고, GitHub에서 요구하는 계정 인증을 완료합니다. 토큰을 소스 파일이나 명령 예시 안에 넣어 저장하지 마세요. 이후 Pages 설정은 위 3번과 같습니다.[2][3]

## 공식 참고

[1]: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
[2]: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
[3]: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
[4]: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
[5]: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
[6]: https://docs.github.com/en/pages/getting-started-with-github-pages/troubleshooting-404-errors-for-github-pages-sites
