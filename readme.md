# 题目-失物招领登记与查询系统

#### 出题人：孙家扬，李承庚

------

## 背景

大学生活中，遗失物品是一个很常见的现象，遗失物品的人通过什么样的途径来查找自己丢失的物品便是一个值得思考的问题；与此同时，对于捡到遗失物品的人来说，如何方便准确地将捡到的物品归还给遗失物品的人，同样是一个值得我们思考的问题。现在把这个问题交给你，请你为遗失物品的人和捡到遗失的物品的人搭建一个桥梁，方便他们查询和登记遗失的物品。

## 你需要做的

你需要设计一个程序，语言不限。基本要求很简单。首先，这个程序能够帮助捡到遗失物品的人**登记**他们捡到的遗失物品。每登记一个物品，需要用户提供**一张图片**，同时提供一些**相关的标签**，便于后续的查找。其次，这个程序还需要帮助遗失物品的人根据他们的**描述**来查找已登记的物品，即输入相应的标签，返回包含有这个标签的图片。

我们使用Python的tkinter库写了一个样例程序（见下）。这个样例实现了基本的登记物品和查找物品。如果你不想白手起家，那么你也可以在我们写好的样例程序上面进行**升级**。升级内容不限，你可以选择改进界面，让界面更加丰富；你也可以选择增加其中的功能，使其更加完善；等等。

## 提高

到此，这是一个本地的后端的程序。我们知道，这样的登记查询系统如果建立在网站上将会更加有意义。请尝试将该系统建立到网站上。

## 挑战

这个程序的查询当前还限制在标签的查询。你有没有什么想法或办法，不通过标签，直接输入相关描述，返回相关的图片？

----

## [样例程序（lcg-wow页面）](https://github.com/lcg-wow/Simple-lost-and-found-management-system)
## [样例程序（BlueberryOreo页面）](https://github.com/BlueberryOreo/Simple-lost-and-found-management-system)

