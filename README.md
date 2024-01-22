# 파일 취합 페이지

# 목차
[프로젝트 개요](#프로젝트-개요)

[기술 스택](#기술-스택)

[주요 기능](#주요-기능)

- [자료 취합 게시판](##자료-취합-게시판)
- [자료 취합 및 통합 양식 검증](##자료-취합-및-통합-양식-검증)
- [인증 코드 생성 및 이메일 발송](##인증-코드-생성-및-이메일-발송)
   
[문제 해결](#문제-해결)

- [고객의 추상적인 요구사항](###고객의-추상적인-요구사항)
- [게시글 수정 보안 문제 해결](###게시글-수정-보안-문제-해결)
- [비밀번호 변경 페이지의 URL 접속](###비밀번호-변경-페이지의-URL-접속)
- [이메일 인증 관련 데이터의 저장 방식](###이메일-인증-관련-데이터의-저장-방식)

# **프로젝트** 개요

해당 웹 프로젝트는 코멘토에서 주어진 과제를 기반으로 진행된 프로젝트로, 다음과 같은 2가지 상황에 대응하기 위해 개발되었다.

### **1. 기존 웹 사이트에 자료 취합 기능 추가**

- **상황**: 이미 존재하는 웹 사이트에 자료 취합 기능을 추가해야 하는 요구사항이 있다.
- **문제**: 이메일을 통한 자료 처리가 어려운 1만여개의 자료가 있다.
- **해결책**: 엑셀 파일 형식의 자료를 취합하며, 자료는 회사 코드, 회사명, 일자, 매출액, 영업이익, 매출액으로 구성된다.

### **2. 취합된 자료를 데이터 별로 통합하는 기능 추가**

- **상황**: 취합된 자료를 데이터 단위로 효과적으로 통합해야 하는 요구사항이 있다.
- **문제**: 여러 엑셀 파일들을 하나의 파일로 통합해야 했으며, 양식에 맞지 않는 데이터가 있는 파일은 통합에서 제외해야 했다.
- **해결책**: 취합된 엑셀 파일들을 하나의 파일로 효과적으로 통합하며, 양식에 맞지 않는 데이터가 있는 파일은 통합 작업에서 배제되었다.

# **기술 스택**

- **FrameWork** : Django
- **Language** : Python
- **DataBase** : MySQL
- **Tool** : Visual Studio Code, Git

# **주요 기능**

## 1. **자료 취합 게시판**

- 사용자들은 첨부 파일을 업로드할 수 있는 게시판을 이용할 수 있으며, 업로드된 파일은 권한을 갖고 있는 유저만 열람할 수 있다.

## 2. **자료 취합 및 통합 양식 검증**

- 관리자 권한을 가진 유저만이 접근할 수 있다.
- 자료 취합 게시판에 업로드된 첨부 파일들을 취합하고 통합할 수 있다.
- 취합된 파일들 중에서 원하는 파일을 선택하여 다운로드, 자료 통합, 또는 삭제가 가능하다.

## 3. 인증 코드 생성 및 이메일 발송

- 사용자가 입력한 이메일 주소로 인증 코드를 발송하면 자동으로 랜덤한 인증 코드가 생성된다. 이메일과 인증 코드 데이터는 사용자의 세션 데이터에 저장된다.
- 이후 사용자의 입력 코드와 세션에 저장된 인증 코드가 일치하면 이메일 인증이 성공적으로 마무리된다. 이메일 인증이 완료되면 세션 데이터에 인증 여부가 저장되며 사용자는 추가 작업을 진행할 수 있다.

### 3.1. 회원 가입에 적용

- 위에서 구현한 이메일 인증 메소드를 회원가입에 적용하였다. 기존에 단순히 이메일 유일성만 확인했던 이메일에 인증 작업을 추가로 적용함으로서 통해 대량의 가짜 계정 생성이나 타인의 개인정보의 무단 사용을 통한 회원 가입또한 예방할 수 있도록 하였다.

### 3.2. 비밀번호 찾기에 적용

- 이메일 인증을 통해 사용자의 이메일의 유효성을 검증할 수 있고 이것을 비밀번호 찾기에 활용할 수 있다.
- 이메일 인증을 통해 사용자를 확인 후, 유저 토큰을 발행하여 해당 토큰을 URL 파라미터로 비밀번호 변경 페이지로 리다이렉션한다.

# **문제 해결**

### 1. **고객의 추상적인 요구사항**

- **문제 상황**
    
    : 초기에 고객이 제시한 요구 사항이 큰 틀에서만 서술되었고, 자세한 부분(예: 업체별 파일 취합 방식, 파일의 접근 권한 등)이 명확하지 않았다.
    
- **해결**
    
     : 고객과의 중간 미팅을 통해 추가적인 의견을 나누어서 기능 개발의 방향성을 정립하였다.
  
### 2. **게시글 수정 보안 문제 해결**

- **문제 상황**
    
    : 게시판의 일반적인 게시글 수정 및 삭제 권한은 게시글을 작성한 유저에게만 부여되는 것이 일반적이다. 그러나 파일 취합 게시판의 경우 여러 기업에서 게시글을 업로드하며, 소속에 따라 게시글 수정 및 삭제 권한이 부여된다. 그러나 누가 게시글을 수정했는지 명확하지 않으면 보안상의 이슈가 발생할 수 있다.
    
- **해결**
    
    : 이 문제를 해결하기 위해 별도의 편집 로그 테이블을 도입하고, 게시글이 업로드되거나 수정될 때 편집 로그 테이블에 해당 데이터가 기록되도록 하였다. 이러한 접근 방식을 통해 게시글 수정 이력을 추적하고, 누가 언제 어떤 수정을 했는지 명확하게 파악할 수 있다. 또한 이 편집 로그 테이블은 관리자 외에는 수정이 불가능하도록 설정하였다.

### 3. 비밀번호 변경 페이지의 URL 접속

- **문제 상황 1.**

: 비밀번호 변경을 위한 이메일 인증을 완료한 사용자 외의 누군가가 해당 사용자의 ID를 URL 파라미터로 입력하여 비밀번호 변경 페이지에 접속할 수 있었다.

- **문제 상황 2.**
  
: 기존에는 로그인을 통해 인증받지 않은 사용자의 접근 막았지만, 이번의 경우 정상적인 사용자 또한 로그인을 할 수 없기에 기존 방식으로는 해결할 수 없었다.

- **해결 [유저 토큰 도입]**
    
    : 유저 토큰은 이메일 인증을 완료한 사용자만이 가지고 있는 특별한 인증 토큰이다. 토큰 인증 과정은 다음과 같다. 
    
    1. **유저 토큰 생성**: 이메일 인증을 완료한 사용자가 비밀번호 변경 페이지로 리다이렉션되기 직전에, 유저 토큰을 생성한다.
    2. **URL 파라미터로 유저 토큰 전송**: 생성된 유저 토큰은 URL의 파라미터로 함께 전송된다. 이를 통해 접근하려는 사용자는 유저 토큰을 가지고 있어야만 접속이 허용된다.
    3. **유저 토큰을 사용한 검증**: 비밀번호 변경 페이지에서는 받은 유저 토큰을 사용하여 해당 사용자가 올바른 사용자인지 검증한다. 이를 통해 이메일 인증을 완료한 사용자만이 비밀번호를 변경할 수 있게 되었다.
    
    | 방식 | 비밀번호 변경 페이지 URL 패턴 |
    | --- | --- |
    | 기존의 이메일 인증 방식 | user/update/<user_id>/password/ |
    | 새로운 토큰 적용 방식 | user/update/<user_id>/password/<user_token> |

### 4. 이메일 인증 관련 데이터의 저장 방식

- **문제 상황**
    
    : 기존에 사용자의 이메일 인증과 관련된 데이터를 보안상의 이유로 Json 파일에 임시저장하고 있었다. 이는 보안에 취약한 구조였으며, 사용자의 데이터가 쌓일수록 관리가 어렵고, 서버의 성능적인 문제도 야기할 것으로 예상되었다.
    
- **해결**
    
    : 이러한 문제의 해결을 위해 기존의 방식에서 세션 데이터를 사용하여 사용자의 이메일 인증과 관련된 데이터를 임시로 저장하도록 변경하였다. 세션 데이터를 사용함으로서 생기는 이점은 다음과 같다.
    
    1. **보안** : 세션 데이터는 서버 측에서 안전하게 관리되므로 데이터 누출 가능성이 크게 감소한다.
    2. **성능** : 세션 데이터는 서버 메모리에 저장되므로 성능적 이점을 얻을 수 있다.
    3. **세션 데이터 자동 만료** : 세션 자동 만료를 설정하여 한 번 생성된 인증코드의 유효기간을 설정하여 사용자가 일정 기간 동안 인증을 완료하지 않을 경우 데이터의 불필요한 쌓임을 방지할 수 있다. 이는 데이터 관리 효율을 향상시킨다.
