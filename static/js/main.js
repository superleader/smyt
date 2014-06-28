$(function(){
	function add_actions(){
		$('.vDateField').datepicker({dateFormat: 'yy-mm-dd'})   
		
		$('.field_value').click(function(){
			if ($(this).find('.field').length == 1){
				$(this).find('.value').hide()
				$(this).find('.field').show()
				$(this).parent().find('.submit').show()
			}
		})
		
		$('.create_model_form').submit(function(){
			var form = $(this)
	    	form.ajaxSubmit({dataType : 'json', success: function(o) {
	            form.find('.error').empty()
	            if(o.result == 1){
	            	alert(form.attr('model') + ' was successfully created')
	            	document.location.href = '/'			            
	            }else
	                if(typeof(o.errors) != undefined)
	                    for(i in o.errors)
	                        form.find('#' + i + '_error').html(o.errors[i][0]) 
	        }})
	        
	        return false;  
		})
		
		$('.btn_edit').click(function(){
			var fields = {}
			var box = $(this).parent().parent()
			box.find('input').each(function(){
				fields[$(this).attr('name')] = $(this).val()
			})
			$.post('/edit', fields, function(o){
	    		box.prev().find('.error').empty()
	            if(o.result == 1){			            	
	            	box.find('.field').hide()
	            	box.find('.submit').hide()
	            	box.find('.value').each(function(){
	            		$(this).html( $(this).parent().find('.field input').val())
	            	}).show()	
	            }else
	                if(typeof(o.errors) != undefined)
	                    for(i in o.errors)
	                        box.prev().find('#' + i + '_error').html(o.errors[i][0]) 
	        })					
		})
	}
	
	$('.models').click(function(){
		$.get('/get_objects/' + $(this).html(), function(o){
			var html = ''
			html += '<h4>' + o.name + '</h4><table border="1" width="100%"><tr>'
			for(i in o.fields)
				html += '<th>' + o.fields[i].name + '</th>'
			html += '</tr>'
			for(i in o.objects){
				html += '<tr>'
				for(j in o.fields)
					html += '<td id="' + o.fields[j].column + '_error" class="error"></td>'
				html += '</tr>'
				
				html += "<tr>"
				for(j in o.fields){
					var value = o.objects[i][ o.fields[j].column ]
					html += '<td class="field_value" ><span class="value">' + value	+ '</span>'
					if(o.fields[j].name == 'ID')
						html += '<input name="id" type="hidden" value="' + value + '" />'
					else{
						html += '<span class="field" style="display:none"><input value="' + value 
							+'" name="' + o.fields[j].column + '" '
						if(o.fields[j].type == 'DateField')
							html += ' class="vDateField" '
						html +=	'></span>'
					}
					html +='</td>'
				}
				html += '<td class="submit" style="display:none;"><input type="hidden" name="csrfmiddlewaretoken" value="'
					+ csrf_token + '" /><input type="hidden" value="' 
					+ o.name + '" name="model_name" /><button class="btn_edit">Save</button></td></tr>'
			}
			html += '</table><fieldset><legend>New ' + o.name 
				+ "</legend><form class='create_model_form' action='/create' model='" 
				+ o.name + "' method='POST'><input type='hidden' name='csrfmiddlewaretoken' value='"
				+ csrf_token + "' />"
			for(j in o.fields){
				if(o.fields[j].name != 'ID'){
					html += '<div class="error" id="' + o.fields[j].column 
						+ '_error" ></div>' + o.fields[j].name + '<input name="' 
						+ o.fields[j].column + '"'
					if(o.fields[j].type == 'DateField')
						html += ' class="vDateField" '	
					html +=	' />'
				}
			}
			html += '<input type="hidden" value="' + o.name 
				+ '" name="model_name" /><br /><input type="submit" value="Create"/></form></fieldset>'
			$('#data_box').html(html)
			add_actions()						
		})
	})						
})