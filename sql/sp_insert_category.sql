CREATE OR REPLACE PROCEDURE insert_category(
    p_category_name VARCHAR(100),
    p_description TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO categories (
        category_name,
        description,
        is_active
    )
    VALUES (
        p_category_name,
        p_description,
        TRUE
    );
END;
$$;