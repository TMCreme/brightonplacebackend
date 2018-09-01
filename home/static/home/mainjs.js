$(document).ready(function(){
    
    $('.chat_head').click(function(){
        $('.chat_body').slideToggle('slow');
    });


    $('.msg_head').click(function(){
        $('.msg_wrap').slideToggle('slow');
    });
    
    
    $('.success').delay(500).fadeIn('normal', function() {
      $(this).delay(2500).fadeOut();
    });
    
    
    $('.navbar .dropdown-item').on('click', function (e) {
        var $el = $(this).children('.dropdown-toggle');
        var $parent = $el.offsetParent(".dropdown-menu");
        $(this).parent("li").toggleClass('open');

        if (!$parent.parent().hasClass('navbar-nav')) {
            if ($parent.hasClass('show')) {
                $parent.removeClass('show');
                $el.next().removeClass('show');
                $el.next().css({"top": -999, "left": -999});
            } else {
                $parent.parent().find('.show').removeClass('show');
                $parent.addClass('show');
                $el.next().addClass('show');
                $el.next().css({"top": $el[0].offsetTop, "left": $parent.outerWidth() - 4});
            }
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $('.navbar .dropdown').on('hidden.bs.dropdown', function () {
        $(this).find('li.dropdown').removeClass('show open');
        $(this).find('ul.dropdown-menu').removeClass('show open');
    });

    
    
    $('.close_chat').click(function(){
        $('.msg_box').hide();
    });
    
    $('.user').click(function(){
        $('.msg_wrap').show();
        $('.msg_box').show();
        
        var rooName = $(this).text();
        
        var chatsocket = new WebSocket(
            'ws://' + window.location.host +
            '/ws/chat/' + rooName + '/');
            
        
        chatsocket.onopen = function open(){
            console.log('Websockets connection created');
        }
        
        chatsocket.onmessage = function(e) {
            var data = JSON.parse(e.data);
            var message = data['message'];
            document.querySelector('#chat-log').value += (message + '\n');
        }
        
        chatsocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        }
        
        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) { // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        }
        
        document.querySelector('#chat-message-submit').onclick = function(e) {
            var messageInputDom = document.querySelector('#chat-message-input');
            var message = messageInputDom.value;
            
            chatsocket.send(JSON.stringify({
                'message':message
            }))
            
            messageInputDom.value = '';
            
            
            $('<div class="msg_a">'+message+'</div>').insertBefore('.msg_insert');
            $('.msg_body').scrollTop($('.msg_body')[0].scrollHeight);
            
            
        }
        
        
    });
    
    
    
});



