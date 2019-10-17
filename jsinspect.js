function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  att1 = splash:select("#fit_type_2")
  assert(att1:mouse_click())
  att2 = splash:select("#color_name_2")
  assert(att2:mouse_click())
  att03 = splash:select("#dropdown_selected_size_name")
  assert(att03:mouse_click())
  assert(splash:wait(0.5))
  att3 = splash:select("#size_name_14")
  assert(att3:mouse_click())
  assert(splash:wait(1))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end


function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  
  
  att01 = splash:select("#dropdown_selected_size_name")
  assert(att01:mouse_click())
  assert(splash:wait(0.25))
  att1 = splash:select("#size_name_0")
  assert(att1:mouse_click())
  assert(splash:wait(1))
  price = splash:select("#priceblock_ourprice")
 	pr1 = price:text()
  
  att03 = splash:select("#dropdown_selected_size_name")
  assert(att03:mouse_click())
  assert(splash:wait(0.25))
  att3 = splash:select("#size_name_4")
  assert(att3:mouse_click())
  assert(splash:wait(1))
  price = splash:select("#priceblock_ourprice")
 	pr2 = price:text()
  
  return {
    pr1, pr2
  }
end

function () {
  return att1 = document.getElementById("inventory-variation-select-0").value = "992598498"
}





function main(splash, args)
 splash.images_enabled = false
 assert(splash:go(args.url))
 assert(splash:wait(0.5))
 sizeid = {
 '#size_name_0',
 '#size_name_1',
 '#size_name_2',
 '#size_name_3',
 '#size_name_4',
 '#size_name_5',
 '#size_name_6',
 '#size_name_7',
  }
  colorid = {
 		'#color_name_0',
    '#color_name_1',
    '#color_name_2',
    '#color_name_3',
    '#color_name_4',
    '#color_name_5',
    '#color_name_6',
    '#color_name_7',
    '#color_name_8',
  }
  local arr = {}
  for j = 1,9 do
    att1 = splash:select(colorid[j])
    assert(att1:mouse_click())
    assert(splash:wait(0.5))
    for i = 1, 8 do
      att03 = splash:select("#dropdown_selected_size_name")
      assert(att03:mouse_click())
      assert(splash:wait(0.25))
      att3 = splash:select(sizeid[i])
      assert(att3:mouse_click())
      assert(splash:wait(1.3))
      arr[i] = splash:select("#priceblock_ourprice"):text()    
     end
  end
  return{
    arr,
    har = splash:har()
  }
end
"//script[contains(text(), 'register(\"ImageBlockATF\"')]/text()"