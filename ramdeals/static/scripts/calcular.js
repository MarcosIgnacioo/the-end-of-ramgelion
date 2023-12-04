productsInCart = document.querySelectorAll('.item-info')
quantities = document.querySelectorAll('#pq')
subtotals = document.querySelectorAll('.total-price')
for ([p,q,s] of zip(productsInCart, quantities, subtotals)){
    prodcutPrice = parseFloat(p.querySelector('#unit-price').textContent);
    quantity = parseFloat(q.value)
    subtotal = prodcutPrice*quantity
    s.textContent = "$" + subtotal
}
function* zip(arr1, arr2, arr3) {
    for (let i = 0; i < Math.min(arr1.length, arr2.length, arr3.length); i++) {
        yield [arr1[i], arr2[i], arr3[i]];
    }
}