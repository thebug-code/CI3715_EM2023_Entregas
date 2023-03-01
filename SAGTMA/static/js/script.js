// ========== Toast Bootstrap ==========
var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(toastEl => (new bootstrap.Toast(toastEl)))
toastList.forEach(toast => toast.show())