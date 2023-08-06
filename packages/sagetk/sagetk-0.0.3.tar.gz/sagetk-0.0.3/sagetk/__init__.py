from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from html.parser import HTMLParser
from tkinter import ttk
try:
	from PIL import ImageTk, Image
except:
	pass
root=Tk()
g=globals()


#custom functions (library controllers)
def link(file_path):
	file_data=open(file_path, 'r') 
	return file_data.read()

#fonts and display predefined vars
font_fam=''; font_size=11; font_style=''; display_var='grid'


def dataManager(elem,name, val=None,parent=None):
	global font_fam; global font_size; global font_style;
	global display_var;

	#grid system
	if name == 'row':
		try:
			if val != None:
				elem.grid_configure(row=int(val)-1)
			else:
				return elem.cget('row')
		except:
			pass
	if name == 'col' or name == 'column':
		#g_col=int(val)-1
		try:
			elem.grid_configure(column=int(val)-1)
		except:
			pass
	if name == 'rowspan' or name == 'row-span':
		try:
			elem.grid_configure(rowspan=int(val))
		except:
			pass
	if name == 'colspan' or name == 'columnspan' or name== 'col-span':
		try:
			elem.grid_configure(columnspan=int(val))
		except:
			pass
	if name == 'grid-gap-x':
		try:
			#getting the value units
			unit=val[len(val)-2:]
			val=val[:len(val)-2]
			if unit=='em':
				val=val*2
			elem.grid_configure(padx=val)
		except:
			pass
	if name == 'grid-gap-y':
		try:
			#getting the value units
			unit=val[len(val)-2:]
			val=val[:len(val)-2]
			if unit=='em':
				val=val*2
			elem.grid_configure(pady=val)
		except:
			pass
	if name == 'grid-gap':
		try:
			#getting the value units
			unit=val[len(val)-2:]
			val=val[:len(val)-2]
			if unit=='em':
				val=val*2
			elem.grid_configure(padx=val,pady=val)
		except:
			pass
	if name == 'space-around':
		try:
			#getting the value units
			unit=val[len(val)-2:]
			val=val[:len(val)-2]
			if unit=='em':
				val=val*2
			elem.grid_configure(ipadx=val,ipady=val)
		except:
			pass
	if name == 'space-around-x':
		try:
			#getting the value units
			unit=val[len(val)-2:]
			val=val[:len(val)-2]
			if unit=='em':
				val=val*2
			elem.grid_configure(ipadx=val)
		except:
			pass
	if name == 'space-around-y':
		try:
			#getting the value units
			unit=val[len(val)-2:]
			val=val[:len(val)-2]
			if unit=='em':
				val=val*2
			elem.grid_configure(ipady=val)
		except:
			pass
	if name == 'justify-content' or  name == 'align-content':
		try:
			if val == 'top-right':
				val='NE'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'bottom-right':
				val='SE'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'bottom-left':
				val='SW'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'top-left':
				val='NW'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'top-right':
				val='NE'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'top':
				val='N'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'right':
				val='E'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'bottom':
				val='S'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'left':
				val='W'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'vertical' or val == 'fill-y':
				val='N+S'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'horizontal' or val == 'fill-x':
				val='E+W'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'fill-both':
				val='N+E+S+W'
				elem.grid_configure(sticky=exec(val,g))
			if val == 'top-right':
				val='NE'
			elem.grid_configure(sticky=exec(val,g))
		except:
			pass

	#colors
	if name == 'color' or  name == 'fg':
		try:
			if val != None:
				elem.configure(fg=val)
			else:
				return elem.cget('fg')
		except:
			pass
	if name == 'background' or name == 'background-color' or  name == 'bg':
		try:
			if val != None:
				elem.configure(bg=val)
			else:
				return elem.cget('bg')
		except:
			pass
	if name == 'active-background' or name == 'active-bg' or name == 'active-background-color':
		try:
			if val != None:
				elem.configure(activebackground=val)
			else:
				return elem.cget('activebackground')
		except:
			pass
	if name == 'active-color' or name == 'active-fg':
		try:
			if val != None:
				elem.configure(activeforeground=val)
			else:
				return elem.cget('activeforeground')
		except:
			pass
	if name == 'highlight-border-color' or   name == 'highlight-bd-color':
		try:
			if val != None:
				elem.configure(highlightcolor=val)
			else:
				return elem.cget('highlightcolor')
		except:
			pass
	if name == 'select-background' or name == 'select-bg':
		try:
			if val != None:
				elem.configure(selectbackground=val)
			else:
				return elem.cget('selectbackground')
		except:
			pass
	if name == 'select-color' or name == 'select-fg':
		try:
			if val != None:
				elem.configure(selectforeground=val)
			else:
				return elem.cget('selectforeground')
		except:
			pass
	if name == 'disabled-color' or name == 'disabled-fg':
		try:
			if val != None:
				elem.configure(disabledforeground=val)
			else:
				return elem.cget('disabledforeground')
		except:
			pass
	#borders
	if name == 'bd-style' or name == 'border-style':
		try:
			if val != None:
				elem.configure(relief=exec(val,g.upper()))
			else:
				return elem.cget('relief')
		except:
			pass
	if name == 'border-width' or name == 'bd-width':
		try:
			if val != None:
				elem.configure(bd=val.upper())
			else:
				elem.cget('bd')
		except:
			pass
	#events
	if name == 'onclick' and elem.cget('state')!='disabled':
		try:
			elem.bind('<Button-1>',lambda e:exec(val,g,g))
		except:
			pass
	if name == 'onchange':
		explode_ele=str(elem).split('!')
		try:
			for i in explode_ele:
				if  i.startswith('combobox'):
					elem.bind('<<ComboboxSelected>>',lambda e:exec(val,g))
				if  i.startswith('entry'):
					elem.bind('<<Modified>>',lambda e:exec(val,g))
		except:
			pass
	if name == 'oncheck' and elem.cget('state')!='disabled':
		try:
			elem.configure(command=lambda:exec(val,g))
		except:
			pass
	if (name == 'ondoubleclick' or name == 'ondouble-click') and elem.cget('state')!='disabled':
		try:
			elem.bind('<Double-Button-1>', lambda e:exec(val,g))
		except:
			pass
	if (name == 'onmouseenter' or name == 'onmouse-enter') and elem.cget('state')!='disabled':
		try:
			elem.bind('<Enter>',lambda e:exec(val,g))
		except:
			pass
	if (name == 'onmouse-leave' or name == 'onmouseleave' or name == 'onmouse-out' or name == 'onmouseout') and elem.cget('state')!='disabled':
		try:
			elem.bind('<Leave>', lambda e:exec(val,g))
		except:
			pass
	if name == 'onactive' and elem.cget('state')!='disabled':
		try:
			elem.bind('<Activate>', lambda e:exec(val,g))
		except:
			pass
	if (name == 'onbuttonrelease' or name == 'onbutton-release') and elem.cget('state')!='disabled':
		try:
			elem.bind('<ButtonRelease>',lambda e:exec(val,g))
		except:
			pass
	if name == 'onresize' and elem.cget('state')!='disabled':
		try:
			elem.bind('<Configure>',lambda e:exec(val,g))
		except:
			pass
	if name == 'oninctive' and elem.cget('state')!='disabled':
		try:
			elem.bind('<Deactivate>',lambda e:exec(val,g))
		except:
			pass
	if (name == 'ondestroy' or name == 'onexit') and elem.cget('state')!='disabled':
		try:
			elem.bind('<Destroy>', lambda e:exec(val,g))
		except:
			pass
	if name == 'onvisible' and elem.cget('state')!='disabled':
		try:
			elem.bind('<Visibility>',lambda e:exec(val,g))
		except:
			pass
	if name == 'onview' and elem.cget('state')!='disabled':
		try:
			elem.bind('<Expose>',lambda e:exec(val,g))
		except:
			pass
	if name == 'onfocus' and elem.cget('state')!='disabled':
		try:
			elem.bind('<FocusIn>',lambda e:exec(val,g))
		except:
			pass
	if name == 'onblur' and elem.cget('state')!='disabled':
		try:
			elem.bind('<FocusOut>',lambda e:exec(val,g))
		except:
			pass
	if name == 'onkeypress' and elem.cget('state')!='disabled':
		try:
			elem.bind('<KeyPress>',lambda e:exec(val,g))
		except:
			pass
	if name == 'onkeyup' and elem.cget('state')!='disabled':
		try:
			elem.bind('<KeyRelease>',lambda e:exec(val,g))
		except:
			pass
	if (name == 'onmousemove' or name == 'onmouse-move' or name == 'onmouse-over' or name == 'onmouseover') and elem.cget('state')!='disabled':
		try:
			elem.bind('<Motion>',lambda e:exec(val,g))
		except:
			pass
	if (name == 'onhide' or name == 'oninvisible') and elem.cget('state')!='disabled':
		try:
			elem.bind('<Unmap>',lambda e:exec(val,g))
		except:
			pass
	#user defined events (controls)
	if  'oncontrol' in name and elem.cget('state')!='disabled':
		try:
			elem.bind('<Control-'+name.split('-')[1]+'>',lambda e:exec(val,g))
		except:
			pass
			
	#fonts
	if name == 'font-family':
		try:
			if val != None:
				font_fam=val
				elem.configure(font=(font_fam,font_size,font_style))
			else:
				return font_fam
		except:
			pass
	if name == 'font-size':
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				font_size=val
				elem.configure(font=(font_fam,font_size,font_style))
			else:
				return font_size
		except:
			pass
	if name == 'font-style':
		try:
			if val != None:
				font_style=val
				elem.configure(font=(font_fam,font_size,font_style))
			else:
				return font_style
		except:
			pass
	if name == 'font-weight':
		
		try:
			if val != None:
				font_style=val
				elem.configure(font=(font_fam,font_size,font_style))
			else:
				return font_style
		except:
			pass

	#dimentions/geometry
	if name == 'width':
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				elem.configure(width=val)
			else:
				return elem.cget('width')
		except:
			pass
	if name == 'height':
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				elem.configure(height=val)
			else:
				return cget('height')
		except:
			pass
	#paddings
	if name == 'padding-x':
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				elem.configure(padx=val)
			else:
				return elem.cget('padx')
		except:
			pass
	if name == 'padding-y':
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				elem.configure(pady=val)
			else:
				return elem.cget('pady')
		except:
			pass
	if name == 'padding' and ' ' not in val:
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				elem.configure(padx=val,pady=val)
			else:
				padx=elem.cget('padx')
				pady=elem.cget('pady')
				full_padding='padding-x:'+str(padx)+','+'padding-y:'+str(pady)
				return full_padding
		except:
			pass
	if name == 'padding' and ' ' in val and len(val.split(' '))==2:
		try:
			if val != None:
				#getting the  units
				y_unit=val.split(' ')[0][len(val.split(' ')[0])-2:]
				x_unit=val.split(' ')[1][len(val.split(' ')[1])-2:]
				#getting values
				pad_y=val.split(' ')[0][:len(val.split(' ')[0])-2]
				pad_x=val.split(' ')[1][:len(val.split(' ')[1])-2]
				if x_unit=='em':
					pad_x=pad_x*2
				if y_unit=='em':
					pad_y=pad_y*2
				elem.configure(pady=pad_y, padx=pad_x)
			else:
				pass
		except:
			pass
	if name == 'padding' and ' ' in val and len(val.split(' '))==4:
		try:
			#getting the  units
			top_unit=val.split(' ')[0][len(val.split(' ')[0])-2:]
			right_unit=val.split(' ')[1][len(val.split(' ')[1])-2:]
			bottom_unit=val.split(' ')[2][len(val.split(' ')[2])-2:]
			left_unit=val.split(' ')[3][len(val.split(' ')[3])-2:]
			#getting values
			pad_top=val.split(' ')[0][:len(val.split(' ')[0])-2]
			pad_right=val.split(' ')[1][:len(val.split(' ')[1])-2]
			pad_bottom=val.split(' ')[2][:len(val.split(' ')[2])-2]
			pad_left=val.split(' ')[3][:len(val.split(' ')[3])-2]
			if top_unit=='em':
					pad_top=pad_top*2
			if right_unit=='em':
					pad_right=pad_right*2
			if bottom_unit=='em':
					pad_bottom=pad_bottom*2
			if left_unit=='em':
					pad_left=pad_left*2
			elem.configure(pady=(pad_top,pad_bottom), padx=(pad_left, pad_right))
			pass
		except:
			pass

	#Margins
	if name == 'margin-x':
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				elem.grid_configure(padx=val)
			else:
				return elem.cget('padx')
		except:
			pass
	if name == 'margin-y':
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				elem.grid_configure(pady=val)
			else:
				return elem.cget('pady')
		except:
			pass
	if name == 'margin' and ' ' not in val:
		try:
			if val != None:
				#getting the value units
				unit=val[len(val)-2:]
				val=val[:len(val)-2]
				if unit=='em':
					val=val*2
				elem.grid_configure(padx=val,pady=val)
			else:
				pass
				'''margin_x=elem.cget('padx')
				margin_y=elem.cget('pady')
				full_margin='margin-x:'+str(margin_x)+','+'margin-y:'+str(margin_x)
				return full_margin'''
		except:
			pass
	if name == 'margin' and ' ' in val and len(val.split(' '))==2:
		try:
			if val != None:
				#getting the  units
				y_unit=val.split(' ')[0][len(val.split(' ')[0])-2:]
				x_unit=val.split(' ')[1][len(val.split(' ')[1])-2:]
				#getting values
				pad_y=val.split(' ')[0][:len(val.split(' ')[0])-2]
				pad_x=val.split(' ')[1][:len(val.split(' ')[1])-2]
				if x_unit=='em':
					pad_x=pad_x*2
				if y_unit=='em':
					pad_y=pad_y*2
				elem.grid_configure(pady=pad_y, padx=pad_x)
			else:
				pass
		except:
			pass
	if name == 'margin' and ' ' in val and len(val.split(' '))==4:
		try:
			#getting the  units
			top_unit=val.split(' ')[0][len(val.split(' ')[0])-2:]
			right_unit=val.split(' ')[1][len(val.split(' ')[1])-2:]
			bottom_unit=val.split(' ')[2][len(val.split(' ')[2])-2:]
			left_unit=val.split(' ')[3][len(val.split(' ')[3])-2:]
			#getting values
			margin_top=val.split(' ')[0][:len(val.split(' ')[0])-2]
			margin_right=val.split(' ')[1][:len(val.split(' ')[1])-2]
			margin_bottom=val.split(' ')[2][:len(val.split(' ')[2])-2]
			margin_left=val.split(' ')[3][:len(val.split(' ')[3])-2]
			if top_unit=='em':
					margin_top=margin_top*2
			if right_unit=='em':
					margin_right=margin_right*2
			if bottom_unit=='em':
					margin_bottom=margin_bottom*2
			if left_unit=='em':
					margin_left=margin_left*2
			elem.grid_configure(pady=(margin_top,margin_bottom), padx=(margin_left, margin_right))
			pass
		except:
			pass
    

	#text formats
	if name == 'justify':
		try:
			if val != None:
				elem.configure(justify=exec(val,g.upper()))
			else:
				return elem.cget('justify')
		except:
			pass
	if name == 'text-transform':
		try:
			get_txt=elem.cget('text')
			if val != None and (val.lower()=='uppercase' or val.lower()=='upper-case' or val.lower()=='upper'):
				elem.configure(text=get_txt.upper())
			elif val != None and (val.lower()=='lowercase' or val.lower()=='lower-case' or val.lower()=='lower'):
				elem.configure(text=get_txt.lower())
			elif val != None and (val.lower()=='capitalise' or val.lower()=='capitalize'):
				elem.configure(text=get_txt.title())
			elif val != None and (val.lower()=='swapcase' or val.lower()=='swap'):
				elem.configure(text=get_txt.swapcase())
			else:
				if get_txt.isupper():
					return 'uppercase'
				elif get_txt.islower():
					return 'lowercase'
				elif get_txt.istitle():
					return 'capitalize'
				else:
					pass
		except:
			pass
	if name == 'text-align':
		try:
			if val != None:
				if val=='left':
					val='W'
				if val=='right':
					val='E'
				elem.configure(anchor=exec(val,g.upper()))
			else:
				return elem.cget('anchor')
		except:
			pass
	if name == 'text-decoration' or name == 'underline':
		try:
			if val != None:
				if val=='underline' or val=='yes':
					val=len(elem.cget('text'))
					x=0
					while x<val:
						elem.configure(underline=x)
						x+=1
			else:
				return elem.cget('underline')
		except:
			pass
	if  name == 'name':
		try:
			if val != None:
				elem.configure(variable=val)
			else:
				return elem.cget('variable')
		except:
			pass
	if name == 'wrap' or name == 'word-wrap':
		try:
			if val != None:
				if val =='yes' or val =='wrap' or val =='break-word':
					val=elem.cget('width')
					elem.configure(wraplength=val)
				if val =='none' or val =='no':
					val='none'
					elem.configure(wrap=val)
			else:
				return elem.cget('wraplength')
		except:
			pass
    
    #Scroll bar (overflow)
	if name == 'overflow':
		try:
			if val != None and val=='scroll':
				# Create a scrollbar widget for y-axis
				scrollbar_y=Scrollbar(parent, orient='vertical')
				scrollbar_y.grid(row=0, column=1, sticky='NS')
				# Create a scrollbar widget for x-axis
				scrollbar_x=Scrollbar(parent, orient='horizontal')
				scrollbar_x.grid(row=1, column=0, sticky='WE')
				elem.grid_configure(row=0, column=0)
				elem.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set,wrap='none')
				scrollbar_x.configure(command=elem.xview)
				scrollbar_y.configure(command=elem.yview)
			if val != None and val=='hidden':
				scrollbar=Scrollbar(parent)
				scrollbar.grid_remove()
				print(scrollbar)

			if val == None:
				pass
				#return elem.cget('state')
		except:
			pass
	if name == 'overflow-y':
		try:
			if val != None and val=='scroll':
				# Create a scrollbar widget for y-axis
				scrollbar_y=Scrollbar(parent, orient='vertical')
				scrollbar_y.grid(row=0, column=1, sticky='NS')
				elem.grid_configure(row=0, column=0)
				elem.configure(yscrollcommand=scrollbar_y.set)
				scrollbar_y.configure(command=elem.yview)
			else:
				pass
				#return elem.cget('state')
		except:
			pass

	if name == 'overflow-x':
		try:
			if val != None and val=='scroll':
				# Create a scrollbar widget for x-axis
				scrollbar_x=Scrollbar(parent, orient='horizontal')
				scrollbar_x.grid(row=1, column=0, sticky='WE')
				elem.grid_configure(row=0, column=0)
				elem.configure(xscrollcommand=scrollbar_x.set, wrap='none')
				scrollbar_x.configure(command=elem.xview)
			else:
				pass
				#return elem.cget('state')
		except:
			pass

	#buttons and inputs		
	if name == 'state':
		try:
			if val != None:
				elem.configure(state=exec(val,g))
			else:
				return elem.cget('state')
		except:
			pass
	if name == 'disabled':
		try:
			if val != None and val=='true':
				elem.configure(state=DISABLED)
			elif val != None and val=='false':
				elem.configure(state=NORMAL)
			else:
				if  val == None:
					return elem.cget('state')
		except:
			pass
	if name == 'checkbox-color':
		try:
			if val != None:
				elem.configure(selectcolor=val)
			else:
				return elem.cget('selectcolor')
		except:
			pass
	if name == 'indicator':
		try:
			if val != None:
				if val=='on' or val=='true':
					val=1
				if val=='off' or val=='false':
					val=0
				elem.configure(indicatoron=val)
			else:
				return elem.cget('indicatoron')
		except:
			pass	
	if name == 'bitmap':
		try:
			if val != None:
				elem.configure(bitmap=val)
			else:
				return elem.cget('bitmap')
		except:
			pass	
	if name == 'cursor':
		try:
			if val != None:
				if val =='pointer':
					val='hand2'
				elem.configure(cursor=val)
			else:
				return elem.cget('cursor')
		except:
			pass
	if name == 'type' and val=='password':
		try:
			if val != None:
				val='*'
				elem.configure(show=val)
			else:
				elem.cget('show')
		except:
			pass
	if name == 'min':
		try:
			if val != None:
				elem.configure(from_=val)
			else:
				elem.cget('from_')
		except:
			pass
	if name == 'max':
		try:
			if val != None:
				elem.configure(to=val)
			else:
				elem.cget('to')
		except:
			pass
	if name == 'length':
		try:
			if val != None:
				elem.configure(length=val)
			else:
				elem.cget('length')
		except:
			pass

	if name == 'step':
		try:
			if val != None:
				elem.configure(tickinterval=val)
			else:
				elem.cget('tickinterval')
		except:
			pass

	if name == 'orient' or name == 'side':
		try:
			if val != None:
				if val=='x':
					val='horizontal'
				if val=='y':
					val='vertical'
				elem.configure(orient=val)
			else:
				elem.cget('orient')
		except:
			pass
	if name == 'value':
		explode_elem=str(elem).split('!')
		try:
			for i in explode_elem:
				#print(i)
				#textarea
				if val != None and i.startswith('text'):
					elem.delete('1.0', END)
					elem.insert('1.0', val)
				if val == None and i.startswith('text'):
					return elem.get('1.0', END)

				#text inputs
				if val != None and i.startswith('entry'):
					elem.delete(0, END)
					elem.insert(0, val)
				if val == None and i.startswith('entry'):
					return elem.get()

				#range input (scale)
				if val != None and i.startswith('scale'):
					elem.set(val)
				if val == None and i.startswith('scale'):
					return elem.get()

				#select option (combo box)
				if val != None and i.startswith('combobox'):
					elem.delete(0, END)
					elem.insert(0, val)
				if val == None and i.startswith('combobox'):
					return elem.get()	
				#checkbox
				if val != None and i.startswith('checkbutton'):
					elem.configure(onvalue=val)
				if val == None and i.startswith('checkbutton'):
					return elem.cget('onvalue')
				#radio button
				if val != None and i.startswith('radiobutton'):
					elem.configure(value=val)
				if val == None and i.startswith('radiobutton'):
					return elem.cget('value')
		except:
			   pass

	if name == 'appendValue' or name == 'append-value':
		try:
			if val != None:
				elem.insert(END, val)
			else:
				return elem.get()
		except:
			pass
	if name == 'prependValue' or name == 'prepend-value':
		try:
			if val != None:
				elem.insert(0, val)
			else:
				return elem.get()
		except:
			pass

	if name == 'text' or name == 'label':
		try:
			if val != None:
				elem.configure(text=val)
			else:
				return elem.cget('text')
		except:
			pass

	#root elemet settings
	if name=='title':
		try:
			elem.title(val)
		except:
        	  pass
	if name=='icon':
		try:
			elem.iconbitmap(val)
		except:
        	  pass
	if name=='size':
		try:
			elem.geometry(val)
		except:
        	  pass
	if name=='resize' and val=='none':
		try:
			elem.resizable(0,0)	
		except:
        	  pass

    #display data in grid

	if name == 'visibility':
		try:
			if val != None and val=='hidden':
				elem.configure(state='hidden')
			elif val != None and val=='visible':
				elem.configure(state='normal')
			else:
				return elem.cget('state')
		except:
			pass
    
	if name=='display':
		display_var=None
		if val != None and val=='none':
			elem.grid_remove()
			display_var=val
	
		elif val != None and val=='grid':
			display_var=val
			elem.grid()
		else:
			return display_var
	else:
		try:
			elem.grid()
			#elem.columnconfigure(0, weight=1)
			#return 'grid'
		except:
			pass

#Setting STYLES
def setStyle(selector, data):
	try:
		for ele in  elem_dic[selector]:
			split_data=data.split(';')
			for d in split_data:
				get_data_name=d.split(':')[0].strip()
				get_data_value=d.split(':')[1].strip()
				dataManager(ele,get_data_name, get_data_value)
	except:
		print('You have either used a wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')

#Elements dictionary (it stores id, class of elems)
elem_dic={}
image_paths=[]
def document(elem):
	class MyHTMLParser(HTMLParser):
		def __init__(self):
			super().__init__()
			self.result = []
			self.current_tag = None
			self.endtags = []
		def handle_starttag(self, tag, attrs):
			obj = {}
			obj["tag"] = tag
			obj["attrs"] = attrs
			obj["data"] = ""
			self.result.append(obj)
			self.current_tag = obj
    
		def handle_data(self, data):
			if data.strip() and self.current_tag:
				self.current_tag["data"] += data.strip()
		def handle_endtag(self, tag):
			self.endtags.append(tag)
	parser = MyHTMLParser()
	parser.feed(elem)
	elem_index=0;
	section=root
	#count elements
	count_buttons=0; count_sections=0;count_inputs=0;
	count_textareas=0; count_labels=0; count_select=0; count_ol=0; count_ul=0; ol_index=0; ul_index=0; count_ol_items=0; count_ul_items=0; count_images=0; count_menu=0; count_menu_items=0; count_menu_data=0; count_table=0; count_table_headers=0; count_table_data=0; count_table_rows=0;
	block_elem=['section','div','table']
	id_name=None
	count_loops=0
	select_element=None
	ol_element=None
	ul_element=None
	menu_element=None
	menu_label=None;
	select_options=[]
	table_element=None
	table_header=None;
	table_data=None
	list_alphabetical=['a','b','c','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	ol_marker='integer'
	ul_marker='circle'
	list_type=None
	taken_class_names=[]
	for elem in parser.result:
		elem_index=elem_index+1
		inner_data=elem['data']
		text_data=elem['data']
		if '<br>' in elem['data']:
			text_data=text_data.replace('<br>','\n')
		start_tag=elem['tag']
		id_name=None
		elem_tag_name=start_tag
		elem_name=None
		class_name=None
		#Root
		if start_tag == 'root':
			count_sections+=1
			elem_name=root
		#Title
		if start_tag=='title':
			root.title(inner_data)
			elem_name=root

		#style
		if start_tag=='style':
			split_sty=inner_data.replace('\n','').split('}')
			try:
				for sty in split_sty:
					if sty !='':
						ele_selector=sty.split('{')[0]
						styles_data=sty.split('{')[1]
						split_data=styles_data.split(';')
						for d in split_data:
							if d !='':
								get_sty_name=d.split(':')[0].strip()
								get_sty_value=d.split(':')[1].strip()
								for ele in elem_dic[ele_selector]:
									dataManager(ele,get_sty_name, get_sty_value)
			except:
				pass
		#sections (Frame)
		if start_tag in block_elem:
			count_sections+=1
			section=Frame(root)
			elem_name=section
			elem_tag_name='section_'+str(count_sections)

		#inputs (Entry)
		if start_tag=='input':
			count_inputs+=1
			elem_tag_name='input_'+str(count_inputs)
			input_type='text'
			for atr in elem['attrs']:
				if atr[0]=='type' and atr[1]=='checkbox':
					input_type='checkbox'
				elif atr[0]=='type' and atr[1]=='radio':
					input_type='radio'
				elif atr[0]=='type' and atr[1]=='file':
					input_type='file'
				elif atr[0]=='type' and atr[1]=='number':
					input_type='number'
				elif atr[0]=='type' and atr[1]=='color':
					input_type='color'
				elif atr[0]=='type' and atr[1]=='date':
					input_type='date'
				elif atr[0]=='type' and atr[1]=='range':
					input_type='range'
				else:
					pass
			if input_type=='text':
				elem_name=Entry(section)
			elif input_type=='file':
				
				file_frame=Frame(section).grid()
				elem_name=Entry(file_frame)
				elem_name.grid_configure(row=0, column=1)
				def getFilename():
					fname=filedialog.askopenfilename()
					elem_name.insert(0, fname)
				file_btn=Button(file_frame, text='Choose file', command=getFilename, bd=1, relief=GROOVE, cursor='hand2').grid(row=0, column=0)
	            
			elif input_type =='checkbox':
				elem_name=Checkbutton(section)
			elif input_type =='radio':
				elem_name=Radiobutton(section)
			elif input_type =='range':
				elem_name=ttk.Scale(section, from_=0, to=100, orient='horizontal', length=200)
			else:
				pass
		#Text (Labels)
		special_tags=['title','option','select','ul','table','ol','hr','input','textarea','img','br','li','mi','md','sp','tr','td','th','style']
		if len(inner_data.strip())>0 and start_tag not in special_tags and start_tag not in block_elem:
			count_labels+=1
			elem_tag_name='text_'+str(count_labels)
			elem_name=Label(section, text=text_data)
			#Heading tags
			if start_tag=='h1':
				elem_name.configure(font=('sans-serif',32,'bold'))
			if start_tag=='h2':
				elem_name.configure(font=('sans-serif',25,'bold'))
			if start_tag=='h3':
				elem_name.configure(font=('sans-serif',20,'bold'))
			if start_tag=='h4':
				elem_name.configure(font=('sans-serif',17,'bold'))
			if start_tag=='h5':
				elem_name.configure(font=('sans-serif',13,'bold'))
			if start_tag=='h6':
				elem_name.configure(font=('sans-serif',10,'bold'))
			#Bold tag
			if start_tag=='b':
				elem_name.configure(font=('sans-serif',12,'bold'))
			#Italic tag
			if start_tag=='i':
				elem_name.configure(font=('times',12,'italic'))

		#Horizontal line
		if start_tag=='hr':
			line =Frame(section, height=2, bd=1, relief=SUNKEN)
			line.grid(row=1, column=0, columnspan=2, sticky=EW, padx=10, pady=10)
		#Button
		if start_tag=='button':
			count_buttons+=1
			elem_tag_name='button_'+str(count_buttons)
			elem_name=Button(section, text=inner_data)

		#images
		if start_tag=='img':
			count_images+=1
			elem_tag_name='img_'+str(count_images)
			for atr in elem['attrs']:
				if atr[0]=='src' and len(atr[1].strip())>0:
					try:
						image_paths.append(ImageTk.PhotoImage(Image.open(atr[1])))
					except:
						print("Image path or Library Error:\nIt seems like you have either used a wrong image pathname in the src attribute of img "+str(count_images)+" or you have not yet installed the python image library (PIL) called pillow, you can install it by running a: 'pip install pillow' in your command prompt.\n")
				try:
					for img_src in image_paths:
						#image_path=ImageTk.PhotoImage(Image.open(img_src))
						#print(img_src)
						elem_name=Label(section, image=img_src)
				except:
					pass

		#Select (combo box)
		if start_tag=='select':
			select_options.clear()
			count_select+=1
			elem_tag_name='select_'+str(count_select)
			elem_name=ttk.Combobox(section)
			select_element=elem_name
		#setting the select tag with options	
		if start_tag=='option':
			#elem_name=Label(section)
			option_value=inner_data
			for opt_attr in elem['attrs']:
				if opt_attr[0]=='value' and len(opt_attr[1].strip())>0:
					option_value=opt_attr[1]
				if opt_attr[0]=='selected':
					select_element.insert(0, inner_data)
			select_options.append(inner_data)
			select_element.configure(values=select_options)

		#Menu
		if start_tag=='menu':
			count_menu+=1
			elem_tag_name='menu_'+str(count_menu)
			main_menu=Menu(section)
			section.configure(menu=main_menu)
			menu_element=main_menu
		#setting menu items	
		if start_tag=='mi':
			menu_item=None
			menu_item=Menu(menu_element)
			count_menu_items+=1
			elem_tag_name='mi_'+str(count_menu_items)
			for typ in elem['attrs']:
				if typ[0]=='label':
					menu_label=typ[1]
        #setting menu data	
		if start_tag=='md':
			command=None; accelerator=None;
			count_menu_data+=1
			elem_tag_name='md_'+str(count_menu_data)
			for typ in elem['attrs']:
				if typ[0]=='onclick' and  len(typ[1].strip())>0:
					'''split_func=typ[1].split(' ')[0]
					command=exec(split_func[:split_func.find('(')])'''
					command=eval(typ[1],g)
				if typ[0]=='alt' and  len(typ[1].strip())>0:
					accelerator=typ[1]
			menu_item.add_command(label=inner_data,accelerator=accelerator, command=command)
		if start_tag=='sp':
			menu_item.add_separator()

		if parser.endtags[elem_index-1] == 'mi':
			try:
				menu_element.add_cascade(label=menu_label, menu=menu_item)
			except:
				pass

		#table
		if start_tag=='table':
			count_table_headers=0
			count_table_data=0
			count_table_rows=0
			count_table_data=0
			count_table+=1
			elem_tag_name='table_'+str(count_table)
		#setting table rows
		if start_tag=='tr':
			count_table_rows+=1
		#setting table headers	
		if start_tag=='th':
			elem_tag_name='th_'+str(count_table_headers)
			elem_name=Label(section,text=inner_data, font=('sans-serif',10,'bold'))
			elem_name.grid_configure( column=count_table_headers, row=count_table_rows-1)
			count_table_headers+=1
        #setting table data	
		if start_tag=='td':
			count_table_data+=1
			elem_tag_name='td_'+str(count_table_data)
			elem_name=Label(section,text=inner_data)
			elem_name.grid_configure(column=count_table_data-1, row=count_table_rows-1)
			if count_table_data==count_table_headers:
				count_table_data=0

		#Ordered list (List box)
		if start_tag=='ol':
			list_type='ol'
			ol_marker='integer'
			count_ol+=1
			elem_tag_name='ol_'+str(count_ol)
			elem_name=Frame(section, bg='white')
			ol_element=elem_name
			for typ in elem['attrs']:
				if typ[0]=='type' and  len(typ[1].strip())>0:
					ol_marker=typ[1]
		#setting the ol tag with  items	
		if start_tag=='li' and list_type=='ol':
			count_ol_items+=1
			elem_tag_name='li_'+str(count_ol_items)
			elem_name=Label(ol_element, bg='white')
			ol_index+=1
			li_marker=ol_index
			if ol_marker=='a':
				li_marker=list_alphabetical[ol_index-1]
			if ol_marker=='A':
				li_marker=list_alphabetical[ol_index-1].upper()
			if ol_marker=='integer':
				li_marker=ol_index
			elem_name.configure(text=str(li_marker)+ '. '+ inner_data)
		if parser.endtags[count_loops-1] == 'ol':
			ol_element=section

		#Unordered list (List box)
		if start_tag=='ul':
			list_type='ul'
			ul_marker='circle'
			count_ul+=1
			elem_tag_name='ul_'+str(count_ul)
			elem_name=Frame(section, bg='white')
			ul_element=elem_name
			for typ in elem['attrs']:
				if typ[0]=='type' and  len(typ[1].strip())>0:
					ul_marker=typ[1]
		#setting the ul tag with  items	
		if start_tag=='li' and list_type=='ul':
			count_ul_items+=1
			elem_tag_name='li_'+str(count_ul_items)
			elem_name=Label(ul_element, bg='white')
			li_marker='"\u25CF'
			if ul_marker=='triangle':
				li_marker='\u2023'
			if ul_marker=='small-circle':
				li_marker='\u2022'
			elif ul_marker=='square':
				li_marker='\u25A0'
			elif ul_marker=='dot':
				li_marker='\u2024'
			elif ul_marker=='bullet':
				li_marker='\u2219'
			elif ul_marker=='white-bullet':
				li_marker='\u25E6'
			elif ul_marker=='hyphen':
				li_marker='\u2043'
			elif ul_marker=='diamond':
				li_marker='\u204C'
			elif ul_marker=='white-diamond':
				li_marker='\u204D'
			elif ul_marker=='circle':
				li_marker='\u25CF'
			else:
				li_marker='\u25CF'
			elem_name.configure(text=str(li_marker)+ ' '+ inner_data)
		if parser.endtags[count_loops-1] == 'ul':
			ul_element=section
		#Textarea
		if start_tag=='textarea':
			count_textareas+=1
			elem_tag_name='textarea_'+str(count_textareas)
			textarea_frame=Frame(section).grid()
			elem_name=Text(section, font=('sans-serif',12,'normal'))
			elem_name.insert('1.0', inner_data)
		if len(elem['attrs'])> 0:
			#pushing elements in the dictionary:
			try:
				for i in elem['attrs']:
					#By id
	  				if i[0]=='id' and len(i[1].strip())>0:
	  					id_name='#'+str(i[1])
	  					elem_dic[id_name]=[elem_name]
	  				#by class
	  				if i[0]=='class' and len(i[1].strip())>0:
	  					class_name='.'+str(i[1])
	  					#adding the class name to the taken array
	  					if class_name not in taken_class_names:
	  						taken_class_names.append(class_name)
	  						elem_dic[class_name]=[]
	  					for key in elem_dic:
	  						if key==class_name.lower() and key.startswith('.'):
	  							elem_dic[key].append(elem_name)
                #by tag name
				elem_dic[elem_tag_name]=[elem_name]

				for attr in elem['attrs']:
	  				attr_name=attr[0].strip()
	  				attr_value=attr[1].strip()
	  				if attr[0]=='style':
	  					split_style=attr[1].split(';')
	  					for style in split_style:
	  						attr_name=style.split(':')[0].strip()
	  						attr_value=style.split(':')[1].strip()
	  						dataManager(elem_name,attr_name.lower(), attr_value,section)
	  				dataManager(elem_name,attr_name.lower(), attr_value, section)
			except:
				pass
		else:
			dataManager(elem_name,'', '')

		if parser.endtags[count_loops-1] in block_elem:
			section=root
		count_loops+=1

#library functions

#getting data
def getData(selector, name):
	try:
		return dataManager(elem_dic[selector][0],name)
	except:
		print('You have either used a wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass
#setting data
def setData(selector, data):
	try:
		for ele in  elem_dic[selector]:
			split_data=data.split(';')
			for d in split_data:
				get_data_name=d.split('=')[0].strip()
				get_data_value=d.split('=')[1].strip()
				dataManager(ele, get_data_name, get_data_value)
	except:
		print('You have either used a wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass

#event listeners

def on(selector, obj, glob=globals()):
	for eve, func, in zip(obj, obj.values()):
		ev='on'+str(eve)
		#dataManager(elem_dic[selector],ev, func)
		#events
	for element in elem_dic[selector]:
		if ev == 'onclick' and element.cget('state')!='disabled':
			try:
				element.bind('<Button-1>',lambda e:exec(func,g,g))
			except:
				pass
		if ev == 'onchange' and element.cget('state')!='disabled':
			explode_ele=str(element).split('!')
			try:
				for i in explode_ele:
					if  i.startswith('combobox'):
						element.bind('<<ComboboxSelected>>',lambda e:exec(func,g))
					if  i.startswith('entry'):
						element.bind('<<Modified>>',lambda e:exec(func,g))
			except:
				pass
		if ev == 'oncheck' and element.cget('state')!='disabled':
			try:
				element.configure(command=lambda e:exec(func,g))
			except:
				pass
		if (ev == 'ondoubleclick' or ev == 'ondouble-click') and element.cget('state')!='disabled':
			try:
				element.bind('<Double-Button-1>',lambda e:exec(func,g))
			except:
				pass
		if (ev == 'onmouseenter' or ev == 'onmouse-enter') and element.cget('state')!='disabled':
			try:
				elem_dic[selector].bind('<Enter>',lambda e:exec(func,g))
			except:
				pass
		if (ev == 'onmouse-leave' or ev == 'onmouseleave' or ev == 'onmouse-out' or ev == 'onmouseout') and element.cget('state')!='disabled':
			try:
				element.bind('<Leave>',lambda e:exec(func,g))
			except:
				pass
		if ev == 'onactive' and element.cget('state')!='disabled':
			try:
				element.bind('<Activate>', lambda e:exec(func,g))
			except:
				pass
		if (ev == 'onbuttonrelease' or ev == 'onbutton-release') and element.cget('state')!='disabled':
			try:
				element.bind('<ButtonRelease>', lambda e:exec(func,g))
			except:
				pass

		if ev == 'onresize' and element.cget('state')!='disabled':
			try:
				element.bind('<Configure>', lambda e:exec(func,g))
			except:
				pass
		if ev == 'oninctive' and element.cget('state')!='disabled':
			try:
				element.bind('<Deactivate>', lambda e:exec(func,g))
			except:
				pass
		if (ev == 'ondestroy' or ev == 'onexit') and element.cget('state')!='disabled':
			try:
				element.bind('<Destroy>', lambda e:exec(func,g))
			except:
				pass
		if ev == 'onvisible' and element.cget('state')!='disabled':
			try:
				element.bind('<Visibility>', lambda e:exec(func,g))
			except:
				pass
		if ev == 'onview' and element.cget('state')!='disabled':
			try:
				element.bind('<Expose>', lambda e:exec(func,g))
			except:
				pass
		if ev == 'onfocus' and element.cget('state')!='disabled':
			try:
				element.bind('<FocusIn>', lambda e:exec(func,g))
			except:
				pass
		if ev == 'onblur' and element.cget('state')!='disabled':
			try:
				element.bind('<FocusOut>', lambda e:exec(func,g))
			except:
				pass
		if ev == 'onkeypress' and element.cget('state')!='disabled':
			try:
				element.bind('<KeyPress>', lambda e:exec(func,g))
			except:
				pass
		if ev == 'onkeyup' and element.cget('state')!='disabled':
			try:
				element.bind('<KeyRelease>', lambda e:exec(func,g))
			except:
				pass
		if (ev == 'onmousemove' or ev == 'onmouse-move' or ev == 'onmouse-over' or ev == 'onmouseover') and element.cget('state')!='disabled':
			try:
				element.bind('<Motion>', lambda e:exec(func,g))
			except:
				pass
		if (ev == 'onhide' or ev == 'oninvisible') and element.cget('state')!='disabled':
			try:
				element.bind('<Unmap>', lambda e:exec(func,g))
			except:
				pass
		#user defined events (controls)
		if  'oncontrol' in ev and element.cget('state')!='disabled':
			try:
				element.bind('<Control-'+ev.split('-')[1]+'>', lambda e:exec(func,g))
			except:
				pass
	
#hiding element
def hide(selector):
	try:
		for ele in  elem_dic[selector]:
			dataManager(ele, 'display','none')
	except:
		print('You have either used a  wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass
#showing element
def show(selector):
	try:
		for ele in  elem_dic[selector]:
			dataManager(ele, 'display','grid')
	except:
		print('You have either used a  wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass

#toggle element
def toggle(selector):
	try:
		for ele in  elem_dic[selector]:
			if dataManager(ele, 'display')=='grid':
				dataManager(ele, 'display','none')
			else:
				dataManager(ele, 'display','grid')
	except:
		print('You have used wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass

#getting  input value
def getValue(selector):
	try:
		return dataManager(elem_dic[selector][0], 'value')
	except:
		print('You have used  wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass

#setting  input value
def setValue(selector, val):
	try:
		for ele in  elem_dic[selector]:
			dataManager(ele, 'value',val)
	except:
		print('You have used  wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass
#appending  input value
def appendValue(selector, val):
	try:
		for ele in  elem_dic[selector]:
			dataManager(ele, 'appendValue',val)
	except:
		print('You have used wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass
#prepending  input value
def prependValue(selector, val):
	try:
		for ele in  elem_dic[selector]:
			dataManager(ele, 'prependValue',val)
	except:
		print('You have used wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass
#setting  text
def setText(selector, text):
	try:
		for ele in  elem_dic[selector]:
			if '<br>' in str(text):
				text=text.replace('<br>','\n')
			dataManager(ele, 'text',text)
	except:
		print('You have either used a  wrong selector name: "'+str(selector)+'" or there are just some errors in your codes')
		pass
#setting  text
def getText(selector):
	try:
		return dataManager(elem_dic[selector][0], 'text')
	except:
		print('You have used wrong id name: "'+str(id_name)+'" or there are just some errors in your codes')
		pass


#file system functions
filePath={}

def saveAs(selector):
	try:
		f_path=filedialog.asksaveasfile()
		open(f_path.name,'w').write(getValue(selector))
		filePath[selector]=f_path.name
		setData('#title','title='+f_path.name)
	except:
		pass

def openFile(selector):
	global filePath
	try:  
		f_path=filedialog.askopenfilename()
		file_content=open(f_path,'r').read()
		setValue(selector, file_content)
		filePath[selector]=f_path
		setData('#title','title='+f_path)
	except:
		pass

def saveFile(selector):
	try:
		open(filePath[selector],'w').write(getValue(selector))
	except:
		saveAs(selector)

def openFilename():
	return filedialog.askopenfilename();


#info alerts
def alert(info, title=None):
	return messagebox.showinfo(title, info)


#running tk window
def run():
	return root.mainloop()


#document(html)


#on('.btns', {'click':lambda e:alert('hfrdhsdf')})


#run()