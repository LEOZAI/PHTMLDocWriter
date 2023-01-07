from docWriter import *

html = Tag("html")
head = Tag("head")
body = Tag("body")
styles = Style()

cls1 = StyleClass(".container")
cls1['width'] = "100%"
cls1['height'] = '100%'


cls2 = StyleClass('.container.images')
cls2['width'] = '600px'
cls2['height'] = '400px'

styles.AddStyle(cls1)
styles.AddStyle(cls2)

div1 = Div()
div1.AddAttribute("class", "cls1")
div1.AddAttribute("class", "cls2")
div1.AddAttribute("data", "data1")

body.AddChild(div1)
html.AddChild(head)
html.AddChild(body)
head.AddChild(styles)

ch1 = Div(_closeline=False)
ch1.AddAttribute("class", "front")
div1.AddChild(ch1)
ch2 = Div()
div1.AddChild(ch2)
ch2.AddAttribute("class", "back")
ch2.AddText("Dummy Text")
img1 = SingleTag("img")
img1.AddAttribute("src", "https://abracadabra.png")
ch1.AddChild(img1)
ch2.AddChild(img1)
ch2.AddText("Another dummy text")
print(html.Write(0))