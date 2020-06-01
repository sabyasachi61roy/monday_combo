$(document).ready(function(){
  //Search
  var searchForm = $(".search-form")
  var searchInput = searchForm.find("[name='q']")

  var typingTimer;
  var typingInterval = 500 // 0.5sec
  var searchBtn = searchForm.find("[type='submit']")

  searchInput.keyup(function(event){
    //console.log(event)
    //console.log(searchInput.val())
    clearTimeout(typingTimer)
    typingTimer = setTimeout(performSearch, typingInterval)
  })

  searchInput.keydown(function(event){
    //console.log(event)
    //console.log(searchInput.val())
    clearTimeout(typingTimer)
    // typingTimer = setTimeout(performSearch, typingInterval)
  })

  function doSearch(){
    searchBtn.addClass("disabled")
    searchBtn.html('<i class="fas fa-spinner"></i> Searching...')
  }

  function performSearch(){
    doSearch()
    var query = searchInput.val()
    setTimeout(function(){
      window.location.href='/search/query/?q=' + query
    }, 1000)  // 1sec
  }


  // Cart
  var comboForm = $(".add-ajax")

  comboForm.submit(function(event){
    event.preventDefault();
    // console.log("Form not sending...")
    
    var thisForm = $(this)
    // var actionEndpoint = thisForm.attr("action");
    var actionEndpoint = thisForm.attr("data-endpoint");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();

    // console.log(thisForm.attr("action"), thisForm.attr("method"))
    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        // console.log("success", data)
        // console.log("Added",data.added)
        // console.log("Updated", data.updated)

        var submitSpan = thisForm.find(".submit-span")

        if(data.noUser){
          swal({
            title: "Opps! You are not logged in",
            text: "Redirecting......",
            button: false,
          })
          setTimeout(function(){
            window.location.href='/accounts/login/'
          }, 1000)
        }else{
          if(data.added){
            submitSpan.html('<button type="submit" class="btn btn-success">Add More?</button>')
            swal({
            title: "",
            text: "Added to cart!",
            icon: "success",
            button: "Okay",
          })
          }else{
            if(data.updated){
              submitSpan.html('<button type="submit" class="btn btn-success">Add More?</button>')
            }else{
              submitSpan.html('<button type="submit" class="btn btn-success">Add to Cart</button>')
            }
          }
        }
        
        var cartCount = $(".cart-count")
        cartCount.text(data.ItemCount)
        console.log(data.ItemCount)
        if(window.location.href.indexOf('cart') != -1){
          refreshCart()
        }
      },
      error: function(errorData){
        if(data.user){
          swal({
            title: "Opps!",
            text: "Login",
            icon: "error",
            button: "Okay",
          })
        }
        
        // alert("An error occured")
        // $.alert("An error occured")
        // swal("Error!","An error occurred", "error")
        // $.alert({
        //   title: "Opps!",
        //   content: "An error occurred.",
        //   theme: "modern",

        // })
        // swal({
        //   title: "Opps!",
        //   text: "An error occured!",
        //   icon: "warning",
        //   dangerMode: true,
        //   button: "Okay",
        // })
        swal({
          title: "Opps!",
          text: "An error occured!",
          icon: "error",
          button: "Okay",
        })
        
        console.log("No API")
        console.log("error", errorData)
      }
    })

  })

  function refreshCart(){
    console.log("In current cart")
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    var comboRows = cartBody.find(".combo-body")
    var addonRows = cartBody.find(".addon-body")
    var currentURL = window.location.href
    // cartBody.html("<h1>Changed</h1>")
    var refresCartURL = '/carts/cart/api/';
    var refreshCartMethod = "GET";
    var data = {};
    $.ajax({
      url: refresCartURL,
      method: refreshCartMethod,
      data: data,
      success: function(data){
        console.log("Success")
        console.log(data)
        if((data.addon.length > 0) || (data.combo.length > 0)){
            // comboRows.html("")
            // $.each(data.combo, function(index, value){
            //   console.log(vakue)
            //   comboRows.prepend("<tr>" + "<td>" + value.title + "</td><td>" + value.price + "</td><td>" + value.sale + "</td><td>" + value.quantity + "</td><td>" + value.combo_total + value.saved + "</td></tr>")
            // })
            // addonRows.html("")
            // $.each(data.addon, function(index, value){
            //   console.log(value)
            //   addonRows.append("<tr>" + "<td>" + value.name + "</td><td>" + value.price + "</td><td></td><td>" + value.quantity + "</td><td>" + value.addon_total + "</td></tr>" )
            // })
            window.location.href = currentURL
        }else{
          window.location.href = currentURL
        }
      },
      error: function(errorData){
        swal({
          title: "Opps!",
          text: "An error occured!",
          button: "Okay",
        })
        console.log("error", errorData)
      }
    })
  }

})