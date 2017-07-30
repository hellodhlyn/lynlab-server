$(document).ready(function () {
    $('.action-modify.button').on('click', function () {
        var transactionId = $(this).data('transactionId');
        $.ajax('/moneybook/modify/' + transactionId)
            .done(function (html) {
                var modal = $('#modify-modal');
                modal.html(html);
                modal.modal({
                    onApprove: function () {
                        $('#form-modify').submit();
                    }
                }).modal('show');
            });
    });
});