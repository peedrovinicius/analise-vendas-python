        revenue=("price", "sum"),
        orders=("order_id", "nunique"),
        items=("order_item_id", "size"),
    )
    .sort_values("revenue", ascending=False)
)
result["average_order_value"] = result["revenue"].div(result["orders"])
result["items_per_order"] = result["items"].div(result["orders"])
result["customer_segment"] = result["orders"].gt(1).map({True: "repeat", False: "one_time"})
return result

