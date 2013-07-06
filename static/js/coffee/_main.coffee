$ ->
    # autocomplete on search
    $('search').typeahead
        minLength: 1
        items: 10
        source: (query, process) ->
            $.get '/s', q: query, (data) ->
                process(data)
            , 'json'

    # enable datepicker for birthday
    $('#id_birthday').datepicker
        changeYear: true
        changeMonth: true
        defaultDate: -(18 * 365)

    # enable & disable submit comment button
    $('#id_comment').keyup ->
        text = $(this).val
        if text is '' or text.length > 300 or text is "Write your review about this movie here" or text is "Leave your comment here"
            $('.submit-post').attr 'disable', true
            if text.length > 300
                $(this).css 'background', '#E3596B'
        else
            $('.submit-post').attr 'disable', false

    #
    $('#id_comment').focus ->
        if $(this).val() is "Write your review about this movie here" or $(this).val() is "Leave your comment here"
            $(this).val ''

    # edit review
    $('#edit-review').click ->
        $('#edit-review-dialog').dialog
            title: 'Edit your review'
            show: 'drop'
            modal: true

    # toggle new movies
    $('#new-movies-btn').click ->
        $('#new-movies').slideDown()

    $('.js-addToFavList').click (e) ->
        e.preventDefault()

        idPair = $(this).attr('id').replace('movie_', '').split('_')
        console.log(idPair)
        movieId = idPair[0]
        userId = idPair[1]
        $.ajax
            url: '/favorite/add'
            type: 'GET'
            data:
                user_id: userId
                movie_id: movieId
            success: (resp) ->
                if resp.result is 'Added successfully'
                    alert 'Added'



    # last return
    true
