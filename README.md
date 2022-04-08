## 프로그램 설명

마크다운으로 된 파일을 명령어(cli) 로 티스토리에 발행한다.

### 지원기능

1. markdown 내의 파일들 티스토리 업로드 및 업로드 파일링크 관리
2. 여러 blog 동시 운영
3. 다른 markdown 과의 링크
4. 폴더 스캔후 md 파일들을 복수발행

### 요구사항

- python version 3.6 이상
- OS : windows or linux 

## 프로그램 설치 및 실행

### 설치

pip 명령어를 이용하여 sub module 을 설치한다.

```sh
pip install markdown
pip install python-frontmatter
pip install markdown-captions
pip install click
```

혹은 requirements.txt 로 설치

```sh
pip install -r requirements.txt
```

### 사용법

> - 프로그램을 사용하기 위해서는 두가지 선행작업이 필요하다.
>   - 환경설정 `config.ini` 설정하기 : [링크](https://github.com/kksworks/tistory-posting-cli/blob/main/README.md#configini)
>   - 마크다운파일의 front matter 설정하기 : [링크](https://github.com/kksworks/tistory-posting-cli/blob/main/README.md#front-matter)

위의 선행작업이 완료한 후에 커맨드라인을 통해서 발행한다. (`--help` 를 통해서 지원되는 옵션과 간단한 명령어 사용법 확인가능하다.)

```sh
$$ python ./tistory_posting_cli.py --help
Usage: tistory_posting_cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get-info  get tistory info
  publish   markdown publish tool for tistory webpage
```

#### get-info 명령어

블로그의 카테고리 정보를 획득한다.

```sh
python ./tistory_posting_cli.py get-info -c [your_blog_name]
```

- `[your_blog_name]` : 카테고리 획득을 위한 타겟 블로그의 이름을 기입

해당명령어가 정상적으로 수행할경우 `meta/tistory-category.json` 에 블로그 카테고리 정보가 생성된다.

> - `meta/tistory-category.json` 의 내용은 포스팅의 front matter 의 category 정보로 활용된다.
> - 글 작성시 `meta/tistory-category.json` 파일이 없을경우 자동으로 해당 명령어가 수행되므로 해당 명령어는 필수가 아니다.

#### pulish 명령어

블로그를 포스팅한다.

```sh
python ./tistory_posting_cli.py publish [makdown_file or folder]
```

- `[makdown_file or folder]` : 발행하고자 하는 마크다운의 파일명 혹은 폴더명을 기입한다.
  - 파일명 입력시 : 1개의 파일만 발행
  - 폴더명 입력시 : 해당 폴더를 순차적으로 마크다운 파일을 탐색하여 발행

마크다운을 포스팅하기위해서는 포스팅을 위한 front matter 정보가 필요하다. [링크](https://github.com/kksworks/tistory-posting-cli/blob/main/README.md#front-matter)

### 동작 테스트

`test_sample` 의 마크다운파일들을 통해서 동작테스트가 가능하다.

- <https://github.com/kksworks/tistory-posting-cli/test_sample> 내의 파일들의 front matter 에서 다음의 내용들을 수정한다.
  - `blog_name:` : 테스트하려는 티스토리 블로그이름
  - `category:` : 게시하려는 카테고리의 이름

다음의 명령어와 같이 입력한 후에 정상적으로 포스팅이 되는지 확인해보자.

```sh
python ./tistory_posting_cli.py publish ./test_sample/test_case-base-md.md
python ./tistory_posting_cli.py publish ./test_sample/test_case-attach-img.md
python ./tistory_posting_cli.py publish ./test_sample/test_case-link-other-md.md
```

- 테스트내용
  - `test_case-base-md.md` : 기본 포스팅테스트
  - `test_case-attach-img.md` : 파일 첨부 테스트
  - `test_case-link-other-md.md` : 마크다운간 포스팅 링크 테스트

## 동작에 관한 설정

### config.ini 

프로그램 동작을 위한 config.ini 을 설정해야한다.

#### tistory section

티스토리에서 api key 를 발급받아 기입한다. 발급방법은 구글링 ㄱㄱ

```ini
[tistory]
tistory_api_key=your_tistory_api_key_string
```

### markdown section

마트다운 파서에 대한 설정을 한다

```ini
[markdown]
folder_chk_exclude_pattern=.git, .ssh
attach_chk_include_pattern=.jpg, .png, .jpeg
attach_chk_exclude_pattern=https://, http://
# attach_retry_cnt=10 # TODO
# save to html convert result
#  - option : [0:no save html, 1:md same path, 2:temp path(./html_tmp)] 
save_conv_html=0
```

- `folder_chk_exclude_pattern` : 폴더 검색시 제외 되어야하는 폴더들 명시
- `attach_chk_include_pattern` : 파일링크에서 자동으로 업로드 되어야하는 파일 확장자
- `attach_chk_exclude_pattern` : 파일링크에서 제외 되어야하는 링크들 (예를들면, 기존 웹링크)
- `save_conv_html` : 마크다운에서 html 변환시 변환된 html 코드를 저장할지 말지 결정
  - 지원 값
    - `0` : html 변환코드를 저장하지 않는다.
    - `1` : html 로 변환된 코드를 `md` 파일과 같은 경로에 저장한다.
    - `2` : html 로 변환된 코드를 `html_tmp` 폴더 경로에 저장한다.

#### log section

프로그램의 로그를 설정한다.

```ini
[log]
log_to_file_path=./debug.log
log_file_max_size_kb=0
# debug , info, error
log_level=debug 
```

- `log_to_file_path` : 로그 파일 남기는 경로. `log_file_max_size_kb` 의 값이 0 이상일때 만 유효
- `log_file_max_size_kb` : 로그파일의 최대 크기
- `log_level` : 로그레벨 설정
  - 지원 값
    - `debug`
    - `info`
    - `error`

#### md_parser_plugin section

markdown 의 내용을 수정/변경하도록 하는 기능을 수행한다.

명시 순서대로 동작을 하며, `true`, `false` 를 통해서 동작여부를 결정할 수있다.

```ini
[md_parser_plugin]
obsidian_wiki_link_conv=false
insert_md_toc=true
obsidian_admonition=true
tistory_file_attach=true
tistory_link_other_md=true
insert_publish_info=true
```

- `obsidian_wiki_link_conv` : obsidian 의 wiki link 를 markdown link 으로 변경 (현재 구현중)
- `insert_md_toc` : 티스토리에 포스팅할때 상단에 table of contents 를 강제로 삽입한다.
- `obsidian_admonition` : obsidian 의 `admonition plug-in` code block 을 변환한다.
- `tistory_file_attach` : markdown 내의 파일링크(그림첨부)등을 티스토리에 자동 업로드한다.
- `tistory_link_other_md` : markdown 내의 다른 티스토리 포스팅을 자동으로 링크한다.
- `insert_publish_info` : 포스팅의 끝에 자동으로 발행정보를 삽입한다. 
  - 지원 값
    - `0` : html 변환코드를 저장하지 않는다.
    - `1` : html 로 변환된 코드를 `md` 파일과 같은 경로에 저장한다.
    - `2` : html 로 변환된 코드를 `html_tmp` 폴더 경로에 저장한다.
  - 참고사항
    - front matter 내의 `save_conv_html` 가 우선한다.


### front matter

tistory 하위 키에 다음의 키을 지원한다.

#### 필수 항목

다음의 항목은 `tistory` 하위에 필수로 있어야 발행 동작을 한다. (없을경우 convert 를 하지 않는다.)

설정예제

```yml
---
tistory:
  blog_name: xenostudy
  category: SW 개발
  publish: true
  tags:
  - test1
  - test2
  title: 'test page : markdown convert test'
---
```

항목설명

- `blog_name` : string
  - 설명
    - 블로그이름을 작성한다. `http://[your_blog_name].tistory.com` 에서 `your_blog_name` 을 작성하면된다.
    - 여러 블로그를 운영하는경우가 있기때문에 따로 옵션으로 구현
- `category` : string or int
  - 설명
    - 발행할 카테고리를 정한다.
    - category 의 code 숫자 값으로 입력하거나, category 명을 직접 입력한다.
    - category 의 실제 code 숫자등의 정보는 `meta/tistory-category.json` 에서 확인가능
- `publish` : boolean
  - 설명 
    - 해당 글을 티스토리로 발행할지 말지 결정한다.
    - 이미 발행된 글을 비공개로 전환하는것이 아니라, 해당 `md` 파일을 티스토리 발행기능을 실행할지 말지를 결정한다.
    - 티스토리에서의 비공개 발행은 지원하지 않는다.
  - 지원 값
    - `true` : 해당 포스팅을 발행한다.
    - `false` : 해당 포스팅을 발행하지 않는다. (로컬로만 저장)
- `tags` : string list
  - 설명
    - 포스팅의 tag 을 지정한다.
- `title` : string
  - 설명
    - 포스팅 타이틀 
    - 만약 `[] : ` 와같은 특수문자를 사용하려면.. `title: '[특수] : 문자' ` 와 같이 `'` 를 사용하여 문자열을 작성한다.

#### 옵션항목

동작과 관련한 옵션항목을 설정한다. 해당 항목들은 없을 경우 기본값(`config.ini` 설정값) 으로 동작한다.

설정예제

```yml
---
tistory:
  blog_name: xenostudy
  category: SW 개발
  publish: true
  tags:
  - test1
  - test2
  title: 'test page : markdown convert test'
  force_chk: true
  save_conv_html: 1
---
```

항목설명

- `force_chk` : boolean - [true / false]
  - 설명
    - 수정된 `md` 파일일 경우(md5로 확인)만 포스팅을 변환/발행하게된다. 즉, `md` 파일이 수정되지 않은 경우는 변환/발행 동작을 스킵하게된다.
    - 강제로 해당 포스팅을 발행할지 말지 결정한다.
    - `publish`이 우선한다. 즉 `publish: false` 로 세팅했을 경우 해당 키는 무시된다.
  - 지원 값
    - `true` : 수정과 관계없이 바로 변환/발행
    - `false` : 수정된 포스팅만 변환/발행
- `save_conv_html` : int 
  - 설명
    - `html` 로 변환한 파일을 저장한다.
    - 해당 옵션은 `config.ini` 의 값보다 우선한다. (만약 해당 키를 작성하지 않을경우 `config.ini` 의 옵션으로 사용한다.)
  - 지원 값
    - `0` : html 변환코드를 저장하지 않는다.
    - `1` : html 로 변환된 코드를 `md` 파일과 같은 경로에 저장한다.
    - `2` : html 로 변환된 코드를 `html_tmp` 폴더 경로에 저장한다.

#### 자동생성되는 항목

포스팅이 완료된경우 front matter 에 다음의 항목들이 자동 생성된다. 수동으로 수정을 하지 않아아야 한다.

포스팅이 완료된후 생성되는 예제

```yml
---
tistory:
  auto_gen:
    md_contents_hash: 69f53bdf3a5007f04a6586e1c8b0109b
    post_id: '714'
    url: https://xenostudy.tistory.com/714
---
```

항목설명

- `md_contents_hash` : font matter 를 제외한 컨텐츠 부분의 md5 hash (수정유무확인)
- `post_id` : 발행이 정상적으로 완료된 경우 포스팅의 `고유 id` 가 기입된다.
- `post_id` : 발행이 정상적으로 완료된 경우 포스틍의 `url` 이 기입된다,


## 동작관련 추가사항

### 파일 첨부(자동업로드)관련

- 파일첨부가 성공할경우, `meta/tistory-attach.json`이 자동생성되며 첨부된 파일명과 url 이 기입된다. 
  - `meta/tistory-attach.json` 파일이 없을경우 파일은 모든 파일을 재 업로드된다.
- 한번 업로드 성공된 파일은 `meta/tistory-attach.json` 파일을 참고하여 재 업로드 하지 않는다.

### 파일 수정 관련

- 한번 발행 성공된 파일은, 마크다운의 내용을 수정을 하지 않으면 업로드 하지 않는다.
- 만약, 재 파싱하여 업로드 하고싶은경우 `md_contents_hash` 부분을 삭제한후에 실행하거나, `force_chk: true` 을 추가하여 실행한다.

### 포스팅의 신규 혹은 수정관련

- 포스팅의 기존 파일수정 혹은 신규업로드의 기준은 front matter 의 `post_id` 를 확인하여 수정한다.
- `post_id` 부분이 없거나, 티스토리 내의 postID 가 존재하지 않을경우, 신규 포스팅으로 간주하여 새로 발행한다.

### 발행된 포스팅의 삭제

- 이미 발행된, 포스팅의 삭제 혹은 비공개로의 전환을 지원하지 않는다. 

### 비공개 포스팅 발행

- 발행하거나 아예 발행하지 않거나만 지원한다. (비공개 포스팅으로의 발행은 미지원)
  - draft 버젼이 필요한경우는 이미 마크다운에 대한 파일이 본인의 컴퓨터에 있으므로 front matter 의 `publish` 부분을 활용하여 발행 진행한다.

## obsidian 에서의 활용

### shell plugin 을 통한 자동 포스팅 만들기

obisian 에서는 shell command 플러그인을 통해서 외부의 스크립트를 실행 할 수있다.

> 단, pc 에 파이썬과 위의 모듈들이 모두 설치되어있어야한다.

- 해당 플러그인 : <https://github.com/Taitava/obsidian-shellcommands>

해당 repo 를 `.obsidian` 폴더 안에 clone 한 후에.. shell command plugin 을 다음과같이 추가한다.

```sh
python {{vault_path}}\.obsidian\tistory-posting-cli\tistory_posting_cli.py publish {{file_path:absolute}}
```

이후에 발행하고자 하는 마크다운파일에서 위의 shell plugin 을 실행 하면 옵시디언에서 바로 티스토리로 포스팅이 가능하다.

## 추가 기능 구현 해야할 사항

- [ ] obsidian wiki link 지원
- [ ] obsidian admonition 변환관련 개선

