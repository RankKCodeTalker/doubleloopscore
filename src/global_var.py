input_template = """问题：“{question}”。
答案1：{answer1}
答案2：{answer2}
对于以上问题，判断答案1和答案2中哪个答案更好。你的回答必须是“答案1更好”、“答案2更好”和“两个答案一样好”其中一个。"""

output_options = ['答案1更好。', '答案2更好。', '两个答案一样好。']