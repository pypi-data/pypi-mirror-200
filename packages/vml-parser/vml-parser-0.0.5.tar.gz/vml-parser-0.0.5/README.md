# vml
## velocitous markup language
(Totally not related with [VML-SVG](https://en.wikipedia.org/wiki/Vector_Markup_Language)\)  
This is a JSON parser for a markup language, if you want to call it like that, that i found myself using while jolting notes in the ~~fastest~~ *most velocitous*, and laziest way that i could think of... It goes pretty much like this:

```
element 1
	things
		dog
		[x] snacks
			[ ] apple
			pear
		house
	names
		james
		alfred

[ ] element 2
	foo
	bar
	baz
```
That translates to this bulky JSON. You see, it makes JSON look bulky!!!
```
[
  {
    "element 1": [
      {
        "things": [
          "dog",
          {
            "snacks": [
              {
                "apple": [],
                "checked": false
              },
              "pear"
            ],
            "checked": true
          },
          "house"
        ]
      },
      {
        "names": [
          "james",
          "alfred"
        ]
      }
    ]
  },
  {
    "element 2": [
      "foo",
      "bar",
      "baz"
    ],
    "checked": false
  }
]
```
vml uses tabs to differentiate the hierarchical level of the current line... i think you got what i mean. Plus, you can also add checkboxes to every line with "[ ]", and you can check it with "[x]", and all this translates to a "checked" property in the JSON representation. It's easy to write vml with vi, for example you might check an empty checkbox with ```rx``` and move around tabulations efficiently with ```>>``` or ```<<```. In fact, this should really have been called tml, as in *tab markup language*, but unfortunately, that resembled too much TOML, dammit you Tom!!  
Install this with ```pip3 install vml-parser```  
Import it with ```from vml_parser import vml```, so you that you can access the ```vml.parse(s : list[str]) -> list[Element]``` method. With that you can easily ```json.loads(str(vml.parse(s : list[str]))) -> object```.  
You will also get the ```vml``` command line script for free! you can pipe it to stdout or you can pass it any number of filenames for it to read.  