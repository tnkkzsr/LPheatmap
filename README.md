# LPheatmap

 
## 起動方法
 
このGithubからクローンし、Dockerのコンテナを起動
```bash
git clone https://github.com/tnkkzsr/LPheatmap.git
cd LPheatmap

docker-compose up --build
```
そして以下のローカルホストにアクセス
```bash
http://0.0.0.0:8000/
```
## 説明
ローカルホストにアクセスすると、このページに飛ぶ




<img width="252" alt="スクリーンショット 2023-06-30 17 48 33" src="https://github.com/tnkkzsr/LPheatmap/assets/107390719/c4b89b29-71fe-4dee-a3e5-33c730040070">　

 「分析するページ」、「アテンションヒートマップ」,「スクロールヒートマップ」、「クリックヒートマップ」はそれぞれリンクとなっており、クリックするとそれぞれが存在するページへ飛ぶ
 
 以下はアテンションヒートマップのところをクリックした例である

 <img width="482" alt="スクリーンショット 2023-06-30 17 52 59" src="https://github.com/tnkkzsr/LPheatmap/assets/107390719/c24e0932-cfe7-409b-8797-ed3ca79418c1">

 ## その他
収集したデータは、 「分析するページ」をクリックしたリンク先のサンプルWebページ上で右クリック→ページを検証→Aplication→LocalStorageで見ることができる

管理者サイトにログインするために必要な情報（ここからも収集データを確認できる）

メールアドレス: tnk30125146@gmail.com

パスワード: lptooladmin


