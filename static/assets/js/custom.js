$(document).ready(function() {
    const dropdownToggle = $('.select-toggle');
    const dropdownMenu = $('.select-menu');
    const dropdownItems = $('.select-option');
  
    // Show or hide the dropdown menu when the toggle is clicked
    dropdownToggle.on('click',function()
    {
        dropdownMenu.toggleClass('show');
        $(this).toggleClass('show');
    })
  
    // // Close the dropdown menu when the user clicks outside of it
    // $(document).click(function(event) {
    //   if (!dropdownMenu.is(event.target) && dropdownMenu.has(event.target).length === 0) {
    //     dropdownMenu.removeClass('show');
    //     dropdownToggle.removeClass('show');
    //   }
    // });
  
    // Update the selected value when an option is clicked
    dropdownItems.click(function() {
      const value = $(this).data('value');
      dropdownToggle.html($(this).html());
      dropdownMenu.removeClass('show');
      dropdownToggle.removeClass('show');
      // Send the selected value to a PHP script using AJAX
      $.ajax({
        type: 'POST',
        url: 'script.php',
        data: { selected: value },
        success: function(response) {
          // PHP script response
          console.log(response);
        }
      });
    });
  });
  
  var nextopt = 0;
function setlimit()
{
    if(nextopt < 0)
    {
        nextopt = 0;
    }
    else if(nextopt >= $('.no-drop-option').length)
    {
        nextopt = $('.no-drop-option').length - 1;
    }
}

//   select without dropdown
$('.bottom_btn').on('click', function()
{
    nextopt++;
    setlimit();
    console.log(nextopt)
    $('.no-drop-option').removeClass('show slide-in slide-out')
    $('.no-drop-option').eq(nextopt).addClass('show')
    $('.no-drop-option').eq(nextopt).addClass('slide-out')




    
})
$('.top_btn').on('click', function()
{
    nextopt--;
    setlimit();
    console.log(nextopt)
    $('.no-drop-option').removeClass('show slide-in slide-out')
    $('.no-drop-option').eq(nextopt).addClass('show')
    $('.no-drop-option').eq(nextopt).addClass('slide-in')

})


$('.emoji img').on("mouseenter", function()
{
    var src = $(this).attr("src").replace('.png', '.gif');
    $(this).attr("src", src);
})
$('.emoji img').on("mouseleave", function()
{
    var src = $(this).attr("src").replace('.gif', '.png');
    $(this).attr("src", src);
})
$('.emoji_img').on('click', function()
{
    $('.emoji').removeClass('active');
    $(this).parent().addClass('active');
})

$('.toggle-onOff').on('click', function()
{
    $(this).toggleClass('active');
})