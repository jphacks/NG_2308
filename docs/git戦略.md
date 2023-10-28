# ブランチ管理

## 特殊ブランチ
- master: 全ての開発用ブランチのmerge先．
- release: masterから派生．常に動作することが保証されている状態．

## 開発用ブランチ
一つのissueにつき一つのブランチを作成．

ブランチは以下の命名規則に従う．

- chrome拡張関係: chrome/{カテゴリ}/{開発する内容を英語で完結に}_#{issue番号}
- engine関係: engine/{カテゴリ}/{開発する内容を英語で完結に}_#{issue番号}
- LLM関係: llm/{カテゴリ}/{開発する内容を英語で完結に}_#{issue番号}
- ドキュメント: docs/{カテゴリ}/{開発する内容を英語で完結に}_#{issue番号}

カテゴリは，
- feature: 新機能開発
- fix: バグ修正

また，ブランチとcommitを紐付けるために，git hookによるcommit massageの変更を行う．

1. リポジトリをclone
2. `$ git config core.hooksPath ".git/hooks"`
3. `.git/hooks/commit-msg` を作って，以下を記載し，実行権限を付与する
```bash
#!/bin/bash
# 参考 https://none-if-none-else-none.hatenablog.com/entry/2020/11/14/000000
issue_num=`git branch --show-current | cut -d/ -f2 | tr -d "\n" | sed -r "s:^.*(#[0-9]+).*$:\1:"`

if [[ $issue_num =~ \#[0-9]* ]]; then
    msg=$(tr -d "\n" < $1)
    echo -n $msg $issue_num > $1
fi
```

# merge
GitHub上でPull requestを出す．
merge先はmasterにして，コメントに close #{issue番号}を含める．
mergeは基本的に澤田が行う．
