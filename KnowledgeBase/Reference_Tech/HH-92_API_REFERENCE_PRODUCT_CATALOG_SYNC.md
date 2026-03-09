---
doc_id: HH-92
title: API Reference — Product Catalog Sync
doc_type: reference
version: 1.0
last_updated: 2026-02-20
---

## Overview
The Product Catalog Sync API allows systems to retrieve, create, and update product information within the retail product catalog. This API is typically used to synchronize product data between inventory systems, ERP platforms, and e-commerce platforms.

---

## Base URL
/api/v1/catalog


---

## Endpoints

### 1. Get Products
Retrieve a list of products from the catalog.

**Endpoint**

GET /catalog/products

**Query Parameters (Optional)**

| Parameter | Type | Description |
|----------|------|-------------|
| category | string | Filter products by category |
| page | integer | Page number for pagination |
| limit | integer | Number of results per page |

**Example Request**

GET /catalog/products?page=1&limit=50


**Example Response**
```json
{
  "products": [
    {
      "product_id": "P1001",
      "name": "Wooden Coffee Table",
      "category": "Furniture",
      "price": 199.99,
      "stock": 45
    }
  ]
}
```

### 2. Create Product

Add a new product to the catalog.

**Endpoint**

POST /catalog/products

**Request Body**

```json
{
  "product_id": "P1002",
  "name": "Modern Floor Lamp",
  "category": "Lighting",
  "price": 89.99,
  "stock": 120,
  "attributes": {
    "color": "black",
    "material": "metal"
  }
}
```

**Response**

```json
{
  "message": "Product created successfully",
  "product_id": "P1002"
}
```

### 3. Update Product (Full Update)

Update all details of an existing product.

**Endpoint**

PUT /catalog/products/{id}

**Path Parameter**


| Parameter | Description |
|----------|-------------|
|id	| Product unique identifier |

**Example Request**

```json
{
  "name": "Modern Floor Lamp",
  "category": "Lighting",
  "price": 79.99,
  "stock": 100,
  "attributes": {
    "color": "black",
    "material": "steel"
  }
}
```

**Response**

```
{
  "message": "Product updated successfully"
}
```

### 4. Partial Update Product

Update specific product fields.

**Endpoint**

PATCH /catalog/products/{id}

**Example Request**
```
{
  "price": 74.99,
  "stock": 90
}
```

**Response**
```
{
  "message": "Product updated successfully"
}
```

**Data Model**

Product Object

|Field	| Type	| Description|
|------|----|----|
|product_id	| string | Unique identifier for the product|
|name	| string	|Product name|
|category|	string|	Product category|
|price|	decimal	|Product selling price|
|stock	|integer|	Available inventory quantity|
|attributes|	object	| Additional product attributes (color, size, material, etc.)|