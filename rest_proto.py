# これにひとまとめでもいいかも
# レストラン用

import restaurant
import recipe

# 1. ユーザーがチャットで打った内容の受付処理



# 2. 楽天APIからカテゴリ一覧を取ってくる処理
L_category = recipe.get_large_category()

# 3. ユーザーに2で取ってきた値を返して、大カテゴリを選んでもらう処理


# 4. 楽天APIから3で受け取った情報をもとに中カテゴリを取ってくる処理
M_category = recipe.get_middle_category()

# 5. ユーザーに2で取ってきた値を返して、中カテゴリを選んでもらう処理


# 6. 5で選んでもらった中カテゴリをもとに、飲食店を検索（位置座標とかはどうなるかわからんけど急いで考えるし調べるちょっと待って）
rest = restaurant.get_restaurant()

# 7. ユーザーに6で取ってきたレストランの情報を返却。記法とか表示処理うんぬんはよくわからん調べる。