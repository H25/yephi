$(document).ready(function() {

    // autocomplete on search
    $('#search-input').typeahead({
        minLength: 1,
        items: 10,
        source: function (query, process) {
            return $.get('/s', { q: query }, function (data) {
                return process(data);
            }, 'json');
        }
    });

    // enable & disable submit review / comment button
    $('#id_comment').keyup(function() {
        var text = $(this).val(),
            submitButton = $(this).parents('form').find('input[type=submit]');

        if (text.length < 3 || text.length > 300) {
            submitButton.attr('disabled', true);

            if (text.length > 300) {
                $(this).css('background', '#fcf8e3'); // change background to yellow if exceed 300 characters
            }
        } else {
            submitButton.attr('disabled', false);
            $(this).css('background', '#fff');
        }
    });

    // add review / comment to feed
    $('.js-submitReviewForm').submit(function() {
        var thisId = $(this).attr('id'),
            idPair = thisId.replace('review_', '').split('_'),
            movieId = idPair[0],
            userId = idPair[1];

        $.ajax({
            url: '/movie/review/',
            type: 'GET',
            dataType: 'json',
            data: {
                user_id: userId,
                movie_id: movieId
            },
            success: function(resp){}
        });
    });
    $('.js-submitCommentForm').submit(function() {
        var thisId = $(this).attr('id'),
            idPair = thisId.replace('comment_', '').split('_'),
            fromUserId = idPair[0],
            toUserId = idPair[1];

        $.ajax({
            url: '/user/commentfeed/',
            type: 'GET',
            dataType: 'json',
            data: {
                f_user: fromUserId,
                t_user: toUserId
            },
            success: function(resp) {}
        });
    });

    // toggle new movies
    $('#new-movies-btn').click(function(e) {
        e.preventDefault();

        $('#new-movies').slideDown();
    });
    $('#new-movies .close').click(function(e) {
        e.preventDefault();

        $('#new-movies').slideUp();
    });

    // add to favorite button
    $('.js-addToFavList').click(function(e) {
        e.preventDefault();

        var thisId = $(this).attr('id'),
            idPair = thisId.replace('movie_', '').split('_'),
            movieId = idPair[0],
            userId = idPair[1];

        $.ajax({
            url: '/favorite/add/',
            type: 'GET',
            dataType: 'json',
            data: {
                user_id: userId,
                movie_id: movieId
            },
            success: function(resp) {
                if (resp.result === 'Added successfully') {
                    window.location.reload();
                }
            }
        });
    });

    // star voting for movie
    $('.js-starsVoting').stars({
        oneVoteOnly: true,
        callback: function(ui, type, value) {
            var thisId = ui.element.attr('id'),
                idPair = thisId.replace('stars_', '').split('_'),
                movieId = idPair[0],
                userId = idPair[1];

            $.ajax({
                url: '/movie/vote/',
                type: 'GET',
                dataType: 'json',
                data: {
                    user_id: userId,
                    movie_id: movieId,
                    rate: value
                },
                success: function (resp) {
                    window.location.reload();
                }
            });
        }
    });

    // enable datepicker for birthday
    $('#id_birthday').datepicker({
        changeYear: true,
        changeMonth: true,
        defaultDate: -(18*365),
        dateFormat: 'yy-mm-dd'
    });


    // user send friend request
    $('.js-sendRequest').click(function(e) {
        e.preventDefault();

        var thisId = $(this).attr('id'),
            idPair = thisId.replace('send_request_', '').split('_'),
            fromId = idPair[0].replace('from', ''),
            toId = idPair[1].replace('to', '');

        $.ajax({
            url: '/user/request/',
            type: 'GET',
            dataType: 'json',
            data: {
                request_type: 'send',
                from_user_id: fromId,
                to_user_id: toId,
                message: 'Hi, may you add me to your friend list?'
            },
            success: function (resp) {
                if (resp.result === 'Sent successfully') {
                    alert('Sent request successfully');
                    $('#'+thisId).hide();
                }
            }
        });
    });

    // user accept friend request
    $('.js-acceptRequest').click(function(e) {
        e.preventDefault();

        var thisId = $(this).attr('id'),
            idPair = thisId.replace('accept_request_', '').split('_'),
            fromId = idPair[0].replace('from', ''),
            toId = idPair[1].replace('to', '');

        $.ajax({
            url: '/user/request/',
            type: 'GET',
            dataType: 'json',
            data: {
                request_type: 'accept',
                from_user_id: fromId,
                to_user_id: toId
            },
            success: function(json){
                alert(json['result']);
                $("#"+thisId).parent().hide();
            }
        });
    });


    // initialize
    var init = function () {
        // change pagination to bootstrap style
        var paginationChildren = $('.pagination ul').children(),
            pagerChildren = $('.pager').children();

        paginationChildren.each(function() {
            $(this).wrap('<li>');
        });
        pagerChildren.each(function() {
            $(this).wrap('<li>');
        });
    };
    init();
});