const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const form = document.getElementById('dataForm');
    if (form) {
        form.addEventListener('submit', productFormOnSubmit);
    }

    const searchButton = document.getElementById('searchButton');
    if (searchButton) {
        
        searchButton.addEventListener('click', searchButtonOnClick);
    }
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const productName = document.getElementById("inputSearch").value;

    fetch(`${api}/search?name=${productName}`)
    .then(response => {

        if (!response.ok) throw new Error('Error!!!');
        return response.json();
    }
)
    .then(products => {
        if (products.length > 0) {
           
            const product = products[0];
            document.getElementById("Cell_Id").textContent = product.id;
            document.getElementById("Cell_Name").textContent = product.name;

            document.getElementById("Cell_Production").textContent = product.production_year;
            document.getElementById("Cell_Price").textContent = product.price;

            document.getElementById("Cell_Color").textContent = product.color;
            document.getElementById("Cell_Size").textContent = product.size;
        } else {
            console.log("No products found.");
        }
    })
    .catch(error => console.error('Error', error));
    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE
    event.preventDefault(); 

    const productData = {
        id: document.getElementById('id').value,
        name: document.getElementById('name').value,
        production_year: parseInt(document.getElementById('production').value, 10),
        price: parseFloat(document.getElementById('price').value),
        color: document.getElementById('color').value,
        size: document.getElementById('size').value
    };

    fetch(`${api}/add-product`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    })
    .then(response => {
        if (!response.ok) throw new Error(`Error ${response.status}`);
        return response.json();
    })
    .then(data => {
        document.getElementById('responseOutput').textContent = `Product added successfully: ${JSON.stringify(data)}`;
    })
    .catch(error => {
        document.getElementById('responseOutput').textContent = `Error adding product: ${error.message}`;
    });
    // END CODE HERE
}
