$(document).ready(function(){

Delete();
View();
New();
Edit();
Search();
CompleteProduct();
CompleteCustomer();
NewTextBox();
AllTotal();
CheckNumbers ();
Total();
Div();
$('.dropdown-toggle').dropdown()
});

function Div()
{
jQuery(function($) {
    $("a.topopup").click(function() {
            loading(); // loading
            setTimeout(function(){ // then show popup, deley in .5 second
                loadPopup(); // function show popup
            }, 500); // .5 second
    return false;
    });
    /* event for close the popup */
    $("div.close").hover(
                    function() {
                        $('span.ecs_tooltip').show();
                    },
                    function () {
                        $('span.ecs_tooltip').hide();
                      }
                );
    $("div.close").click(function() {
        disablePopup();  // function close pop up
    });
    $(this).keyup(function(event) {
        if (event.which == 27) { // 27 is 'Ecs' in the keyboard
            disablePopup();  // function close pop up
        }
    });
    $("div#backgroundPopup").click(function() {
        disablePopup();  // function close pop up
    });
     /************** start: functions. **************/
    function loading() {
        $("div.loader").show();
    }
    function closeloading() {
        $("div.loader").fadeOut('normal');
    }
    var popupStatus = 0; // set value
    function loadPopup() {
        if(popupStatus == 0) { // if value is 0, show popup
            closeloading(); // fadeout loading
            $("#toPopup").fadeIn(0500); // fadein popup div
            $("#backgroundPopup").css("opacity", "0.7"); // css opacity, supports IE7, IE8
            $("#backgroundPopup").fadeIn(0001);
            popupStatus = 1; // and set value to 1
        }
    }
    function disablePopup() {
        if(popupStatus == 1) { // if value is 1, close popup
            $("#toPopup").fadeOut("normal");
            $("#backgroundPopup").fadeOut("normal");
            popupStatus = 0;  // and set value to 0
        }
    }
    /************** end: functions. **************/
}); // jQuery End
}

function View()
    {
        $(document).on("click", ".view" ,function(){
                      location.href = $(this).attr("id");
        });
    }

function New()
    {
        $('#newform').ajaxForm(function(message){
            alert(message.Message);
            $("#latesitemsdiv").load("latest/" , function() {
                $('#newform').trigger('reset');
           });
        });
    }

function Edit()
    {
        $(document).on("click", ".edit" ,function(){
            x = $(this).attr("id");
            //$.get(x ,function(){
                $("#viewarea").load(x , function(){
                      $('.editform').ajaxForm(function(message){
                        alert(message.Message);
                            $("#latesitemsdiv").load("latest/" , function() {
                            $('#newform').trigger('reset');
                            });
                    });
                });
        });
    }

function Delete()
    {
        $(document).on("click", ".delete" ,function(){
            $.get($(this).attr("id"),function(message){
                alert(message.Message)
                    location.reload ();
            });
        });
    }

function Search()
    {
        $(document).on("click", ".searchform" ,function(){
            $('#searchform').ajaxForm(function(message){
                $("#viewarea").html( "Code: " +message.ItemCode + " <br> " +
                            "Name: " +message.ItemName + " <br> " +
                            "Price: " +message.ItemPrice + " <br> " +
                            "Date: " +message.ItemDate + " <br> "
                            );
                    $('#searchform').trigger('reset');
            });
        });

    }

function CompleteProduct(){
$( ".product" ).autocomplete({
        select: function (e, ui) {
            $("#1").val(ui.item.label);
            return false;
        },
        source: function (request, response) {
            var elm_id = $(this.element).prop("id");
            $.ajax({
                url: '/autocompleteproduct/',
                data: request,
                success: function (data) {
                    var ParsedObject = $.parseJSON(data);
                    response($.map(ParsedObject, function (item) {
                        var name = item.fields.product_name ;
                        var price = item.fields.product_price ;
                        var available= item.fields.product_count ;
                        var p_id = item.pk ;
                        return {
                            value: name,
                            p_price: price,
                            p_available: available,
                            p_id: p_id,
                            elm_id: elm_id,
                        }
                    }));
            }
    });
},
    minLength: 1,
  	autoFocus: true,
        select: function ( event, ui ) {
              $('#price_'+ui.item.elm_id).val( ui.item.p_price );
              $('#available_'+ui.item.elm_id).val( ui.item.p_available );
              //$('#id_'+ui.item.elm_id).val( ui.item.p_id );
              AllTotal();
        },
    });
}

function CompleteCustomer(){
$( "#customer_name" ).autocomplete({
        select: function (e, ui) {
            $("#customer_name").val(ui.item.label);
            return false;
        },
        source: function (request, response) {
            $.ajax({
                url: '/autocompletecustomer/',
                data: request,
                success: function (data) {
                    var ParsedObject = $.parseJSON(data);
                    response($.map(ParsedObject, function (item) {
                        var name = item.fields.customer_name ;
                        return {
                            value: name,
                        }
                    }));
            }
    });
},
    minLength: 1,
    });
}

function NewTextBox()
{
AllTotal();
    var counter = 2;
    $("#addButton").click(function () {
	if(counter>50){
            alert("Only 50 textboxes allow");
            return false;
	}
	var newTextBoxTr = $(document.createElement('tr'))
	     .attr("id", 'TextBoxTr' + counter);
	newTextBoxTr.before($()).html('<td><label for="'+ counter+'">'+ counter + ' : </label></td>' +
	 '<td><input type="textbox"  id ="'+ counter+'"name="product_' + counter + '"class="product ui-autocomplete-input" ></td>'+
	 '<td><input type="textbox" name="price_' + counter +'" id="price_' + counter + '" value=""  class="price" readonly></td>'+
	  '<td><input type="textbox" name="available_' + counter +'" id="available_' + counter + '" value="" class="" readonly></td>'+
	  '<td><input type="textbox" name="sell_' + counter +'" id="sell_' + counter + '" value="" class="number" ></td>'+
	  '<td><input type="textbox" name="count_' + counter +'" id="count_' + counter + '" value="" class="number" ></td>'+
	  '<td><input type="textbox" name="total_' + counter +'" id="total_' + counter + '" value="" class="total" readonly></td>');
	newTextBoxTr.insertBefore(".total_price");
	 //location.reload ();
	CompleteProduct();
	AllTotal();
	Total();
	counter++;
     });
     $("#removeButton").click(function () {
	if(counter==2){
          alert("No more textbox to remove");
          return false;
       }
	counter--;
        $("#TextBoxTr" + counter).remove();
     });
     $("#getButtonValue").click(function () {
	var msg = '';
	for(i=1; i<counter; i++){
   	  msg += "\n Textbox #" + i + " : " + $('#count_product_' + i).val();
	}
    	  alert(msg);
     });
  }

function AllTotal()
{
$('.total').change(function () {
    var sum = 0;
    $('.total').each(function() {
        sum += Number($(this).val());
    });
    $('#all_total').val(sum);
});
$('#removeButton').click(function () {
    var sum = 0;
    $('.total').each(function() {
        sum += Number($(this).val());
    });
     CheckNumbers ();
     Total();
    $('#all_total').val(sum);
});
$('#addButton').click(function () {
    var sum = 0;
    $('.total').each(function() {
        sum += Number($(this).val());
        CheckNumbers ();
        Total();
    });
    $('#all_total').val(sum);
});
$('.total').keyup(function () {
    var sum = 0;
    $('.total').each(function() {
        sum += Number($(this).val());
    });
    $('#all_total').val(sum);
});
}

//function Total()
//{
//$("#count_1").change(function () {
//    sum = parseFloat($("#count_1").val())  * parseFloat($("#sell_1").val())  ;
//    $("#total_1").val(sum);
//});
//$("#count_2").change(function () {
//    sum = parseFloat($("#count_2").val())  * parseFloat($("#sell_2").val())  ;
//    $("#total_2").val(sum);
//});
//$("#count_3").change(function () {
//    sum = parseFloat($("#count_3").val())  * parseFloat($("#sell_3").val())  ;
//    $("#total_3").val(sum);
//});
//$("#count_4").change(function () {
//    sum = parseFloat($("#count_4").val())  * parseFloat($("#sell_4").val())  ;
//    $("#total_4").val(sum);
//});
//$("#count_5").change(function () {
//    sum = parseFloat($("#count_5").val())  * parseFloat($("#sell_5").val())  ;
//    $("#total_5").val(sum);
//});
//$("#count_6").change(function () {
//    sum = parseFloat($("#count_6").val())  * parseFloat($("#sell_6").val())  ;
//    $("#total_6").val(sum);
//});
//$("#count_7").change(function () {
//    sum = parseFloat($("#count_7").val())  * parseFloat($("#sell_7").val())  ;
//    $("#total_7").val(sum);
//});
//$("#count_8").change(function () {
//    sum = parseFloat($("#count_8").val())  * parseFloat($("#sell_8").val())  ;
//    $("#total_8").val(sum);
//});
//$("#count_9").change(function () {
//    sum = parseFloat($("#count_9").val())  * parseFloat($("#sell_9").val())  ;
//    $("#total_9").val(sum);
//});
//$("#count_10").change(function () {
//    sum = parseFloat($("#count_10").val())  * parseFloat($("#sell_10").val())  ;
//    $("#total_10").val(sum);
//});
//$("#count_11").change(function () {
//    sum = parseFloat($("#count_11").val())  * parseFloat($("#sell_11").val())  ;
//    $("#total_11").val(sum);
//});
//$("#count_12").change(function () {
//    sum = parseFloat($("#count_12").val())  * parseFloat($("#sell_12").val())  ;
//    $("#total_12").val(sum);
//});
//$("#count_13").change(function () {
//    sum = parseFloat($("#count_13").val())  * parseFloat($("#sell_13").val())  ;
//    $("#total_13").val(sum);
//});
//$("#count_14").change(function () {
//    sum = parseFloat($("#count_14").val())  * parseFloat($("#sell_14").val())  ;
//    $("#total_14").val(sum);
//});
//$("#count_15").change(function () {
//    sum = parseFloat($("#count_15").val())  * parseFloat($("#sell_15").val())  ;
//    $("#total_15").val(sum);
//});
//$("#count_16").change(function () {
//    sum = parseFloat($("#count_16").val())  * parseFloat($("#sell_16").val())  ;
//    $("#total_16").val(sum);
//});
//$("#count_17").change(function () {
//    sum = parseFloat($("#count_17").val())  * parseFloat($("#sell_17").val())  ;
//    $("#total_17").val(sum);
//});
//$("#count_18").change(function () {
//    sum = parseFloat($("#count_18").val())  * parseFloat($("#sell_18").val())  ;
//    $("#total_18").val(sum);
//});
//$("#count_19").change(function () {
//    sum = parseFloat($("#count_19").val())  * parseFloat($("#sell_19").val())  ;
//    $("#total_19").val(sum);
//});
//$("#count_20").change(function () {
//    sum = parseFloat($("#count_20").val())  * parseFloat($("#sell_20").val())  ;
//    $("#total_20").val(sum);
//});
//$("#sell_1").change(function () {
//    sum = parseFloat($("#count_1").val())  * parseFloat($("#sell_1").val())  ;
//    $("#total_1").val(sum);
//});
//$("#sell_2").change(function () {
//    sum = parseFloat($("#count_2").val())  * parseFloat($("#sell_2").val())  ;
//    $("#total_2").val(sum);
//});
//$("#sell_3").change(function () {
//    sum = parseFloat($("#count_3").val())  * parseFloat($("#sell_3").val())  ;
//    $("#total_3").val(sum);
//});
//$("#sell_4").change(function () {
//    sum = parseFloat($("#count_4").val())  * parseFloat($("#sell_4").val())  ;
//    $("#total_4").val(sum);
//});
//$("#sell_5").change(function () {
//    sum = parseFloat($("#count_5").val())  * parseFloat($("#sell_5").val())  ;
//    $("#total_5").val(sum);
//});
//$("#sell_6").change(function () {
//    sum = parseFloat($("#count_6").val())  * parseFloat($("#sell_6").val())  ;
//    $("#total_6").val(sum);
//});
//$("#sell_7").change(function () {
//    sum = parseFloat($("#count_7").val())  * parseFloat($("#sell_7").val())  ;
//    $("#total_7").val(sum);
//});
//$("#sell_8").change(function () {
//    sum = parseFloat($("#count_8").val())  * parseFloat($("#sell_8").val())  ;
//    $("#total_8").val(sum);
//});
//$("#sell_9").change(function () {
//    sum = parseFloat($("#count_9").val())  * parseFloat($("#sell_9").val())  ;
//    $("#total_9").val(sum);
//});
//$("#sell_10").change(function () {
//    sum = parseFloat($("#count_10").val())  * parseFloat($("#sell_10").val())  ;
//    $("#total_10").val(sum);
//});
//$("#sell_11").change(function () {
//    sum = parseFloat($("#count_11").val())  * parseFloat($("#sell_11").val())  ;
//    $("#total_11").val(sum);
//});
//$("#sell_12").change(function () {
//    sum = parseFloat($("#count_12").val())  * parseFloat($("#sell_12").val())  ;
//    $("#total_12").val(sum);
//});
//$("#sell_13").change(function () {
//    sum = parseFloat($("#count_13").val())  * parseFloat($("#sell_13").val())  ;
//    $("#total_13").val(sum);
//});
//$("#sell_14").change(function () {
//    sum = parseFloat($("#count_14").val())  * parseFloat($("#sell_14").val())  ;
//    $("#total_14").val(sum);
//});
//$("#sell_15").change(function () {
//    sum = parseFloat($("#count_15").val())  * parseFloat($("#sell_15").val())  ;
//    $("#total_15").val(sum);
//});
//$("#sell_16").change(function () {
//    sum = parseFloat($("#count_16").val())  * parseFloat($("#sell_16").val())  ;
//    $("#total_16").val(sum);
//});
//$("#sell_17").change(function () {
//    sum = parseFloat($("#count_17").val())  * parseFloat($("#sell_17").val())  ;
//    $("#total_17").val(sum);
//});
//$("#sell_18").change(function () {
//    sum = parseFloat($("#count_18").val())  * parseFloat($("#sell_18").val())  ;
//    $("#total_18").val(sum);
//});
//$("#sell_19").change(function () {
//    sum = parseFloat($("#count_19").val())  * parseFloat($("#sell_19").val())  ;
//    $("#total_19").val(sum);
//});
//$("#sell_20").change(function () {
//    sum = parseFloat($("#count_20").val())  * parseFloat($("#sell_20").val())  ;
//    $("#total_20").val(sum);
//});
//}



function Total()
{
var counter = 1;
var sum = 0;
$("#count_" + counter).change(function () {
    sum = parseFloat($("#count_" + counter).val())  * parseFloat($("#sell_" + counter).val())  ;
    $("#total_" + counter).val(sum);
});
$("#sell_" + counter).change(function () {
    sum = parseFloat($("#count_" + counter).val())  * parseFloat($("#sell_" + counter).val())  ;
    $("#total_" + counter).val(sum);
});
 $("#addButton").click(function () {
    sum = parseFloat($("#count_" + counter).val())  * parseFloat($("#sell_" + counter).val())  ;
    $("#total_" + counter).val(sum);
Total();
counter++;
$("#count_" + counter).change(function () {
    sum = parseFloat($("#count_" + counter).val())  * parseFloat($("#sell_" + counter).val())  ;
    $("#total_" + counter).val(sum);
});$("#sell_" + counter).change(function () {
    sum = parseFloat($("#count_" + counter).val())  * parseFloat($("#sell_" + counter).val())  ;
    $("#total_" + counter).val(sum);
});
});
}

function CheckNumbers ()
{
  //called when key is pressed in textbox
  $(".number").keypress(function (e) {
     //if the letter is not digit then display error and don't type anything
     if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
               return false;
    }
   });
}
//function Complete(){
//$( "#product" ).autocomplete({
//        select: function (e, ui) {
//            $("#product").val(ui.item.label);
//            return false;
//        },
//        source: function (request, response) {
//            $.ajax({
//                url: '/autocomplete',
//                data: request,
//                success: function (data) {
//                    var ParsedObject = $.parseJSON(data);
//                    response($.map(ParsedObject, function (item) {
//                        var name = item.fields.product_name ;
//                        var price = item.fields.product_price ;
//                        var count = item.fields.product_count ;
//                        return {
//                            value: name,
//                            price: price,
//                            count: count,
//                        };
//                    }));
//            }
//    });
//},
//    minLength: 1,
//  	autoFocus: true,
//        select: function ( event, ui ) { // What happens when an autocomplete result is selected
//              $('#price').val( ui.item.price );
//              $('#count').val( ui.item.count );
//        },
//    });
//}
//  $("#product").autocomplete({
//        source: '/autocomplete', // The source of the AJAX results
//        minLength: 1, // The minimum amount of characters that must be typed before the autocomplete is triggered
//        focus: function( event, ui ) { // What happens when an autocomplete result is focused on
//            $("#product").val( ui.fields.product_name );
//            return false;
//      },
//      select: function ( event, ui ) { // What happens when an autocomplete result is selected
//          $("#product").val( ui.fields.product_name );
//          $('#price').val( ui.fields.product_price );
//      }
//  });
//autocomplete script
//$(document).on('focus','.autocomplete_txt',function(){
//	type = $(this).data('type');
//	if(type =='productCode' )autoTypeNo=0;
//	if(type =='productName' )autoTypeNo=1;
//	$(this).autocomplete({
//		source: function( request, response ) {
//			$.ajax({
//				url : 'ajax.php',
//				dataType: "json",
//				method: 'post',
//				data: {
//				   name_startsWith: request.term,
//				   type: type
//				},
//				 success: function( data ) {
//					 response( $.map( data, function( item ) {
//					 	var code = item.split("|");
//						return {
//							label: code[autoTypeNo],
//							value: code[autoTypeNo],
//							data : item
//						}
//					}));
//				}
//			});
//		},
//		autoFocus: true,
//		minLength: 0,
//		select: function( event, ui ) {
//			var names = ui.item.data.split("|");
//			id_arr = $(this).attr('id');
//	  		id = id_arr.split("_");
//	  		element_id = id[id.length-1];
//			$('#itemNo_'+element_id).val(names[0]);
//			$('#itemName_'+element_id).val(names[1]);
//			$('#quantity_'+element_id).val(1);
//			$('#price_'+element_id).val(names[2]);
//			$('#total_'+element_id).val( 1*names[2] );
//			calculateTotal();
//		}
//	});
//});

//function Complete()
//{
//$("#product").autocomplete({
//                source: function( request, response ) {
//                $.ajax({
//                    url: "/autocomplete/",
//                    dataType: "json",
//                    data: {term: request.term},
//                    success: function(data) {
//                     var ParsedObject = $.parseJSON(data);
//                               response($.map(ParsedObject, function (item) {
//                                return {
//                                    value: item.fields.product_name,
//                                    };
//                            }));
//                        }
//                    });
//                },
//                minLength: 1,
//                select: function(event, ui) {
//                    $('#price').val(ui.item.id);
//                }
//            });
//}

//function Complete()
//    {
//$('#product').autocomplete({
//    source: function (request, response) {
//        $.getJSON("/autocomplete/?term=" + request.term, function (data) {
//            response($.map(data.products, function (item) {
//                return {
//                    value: item.fields.product_name
//                };
//            }));
//        });
//    },
//    minLength: 1,
//    delay: 100
//});
//    }

