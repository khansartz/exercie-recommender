# media.py
import os

def get_media_dict():
    # Sesuaikan path folder "media" tempat lo naro gambar/video
    base_path = os.path.join(os.path.dirname(__file__), "media")

    return {
        # Exercises
        "squats": os.path.join(base_path, "squats.jpg"),
        "yoga": os.path.join(base_path, "yoga.jpg"),
        "deadlifts": os.path.join(base_path, "deadlifts.jpg"),
        "bench_presses": os.path.join(base_path, "bench_press.jpg"),
        "overhead_presses": os.path.join(base_path, "overhead_press.jpg"),
        "brisk_walking": os.path.join(base_path, "brisk_walking.jpg"),
        "cycling": os.path.join(base_path, "cycling.jpg"),
        "running": os.path.join(base_path, "running.jpg"),
        "swimming": os.path.join(base_path, "swimming.jpg"),
        "dancing": os.path.join(base_path, "dancing.jpg"),

        # Equipment
        "dumbbells": os.path.join(base_path, "dumbbells.jpg"),
        "resistance_bands": os.path.join(base_path, "resistance_bands.jpg"),
        "barbells": os.path.join(base_path, "barbells.jpg"),
        "a_blood_glucose_monitor": os.path.join(base_path, "blood_glucose_monitor.jpg"), # Digabung
        "light_dumbbells": os.path.join(base_path, "light_dumbbells.jpg"),
        "light_athletic_shoes": os.path.join(base_path, "light_athletic_shoes.jpg"),
        "ellipticals": os.path.join(base_path, "ellipticals.jpg"),
        "indoor_rowers": os.path.join(base_path, "indoor_rowers.jpg"),
        "treadmill": os.path.join(base_path, "treadmills.jpg"), # Key-nya 'treadmill'
        "rowing_machine": os.path.join(base_path, "rowing_machine.jpg"),
        "kettlebell": os.path.join(base_path, "kettlebell.jpg"),
        "yoga_mat": os.path.join(base_path, "yoga_mat.jpg"),

        # Vegetables
        "garlic": os.path.join(base_path, "garlic.jpg"),
        "carrots": os.path.join(base_path, "carrots.jpg"),
        "lettuce": os.path.join(base_path, "lettuce.jpg"),
        "sweet_potato": os.path.join(base_path, "sweet_potato.jpg"),
        "roma_tomatoes": os.path.join(base_path, "roma_tomatoes.jpg"),
        "green_pepper": os.path.join(base_path, "green_pepper.jpg"), # Typo fix
        "tomatoes": os.path.join(base_path, "tomatoes.jpg"),
        "leafy_greens": os.path.join(base_path, "leafy_greens.jpg"),
        "broccoli": os.path.join(base_path, "broccoli.jpg"),
        "capers": os.path.join(base_path, "capers.jpg"),
        "iceberg_lettuce": os.path.join(base_path, "iceberg_lettuce.jpg"),
        "mixed_greens": os.path.join(base_path, "mixed_greens.jpg"),
        "cherry_tomatoes": os.path.join(base_path, "cherry_tomatoes.jpg"),
        "cucumbers": os.path.join(base_path, "cucumbers.jpg"),
        "celery": os.path.join(base_path, "celery.jpg"),
        "mushroom": os.path.join(base_path, "mushroom.jpg"), # Typo fix
        "water_chestnuts": os.path.join(base_path, "water_chestnuts.jpg"),
        "onion": os.path.join(base_path, "onion.jpg"),
        "spinach": os.path.join(base_path, "spinach.jpg"),

        # Protein
        "red_meats": os.path.join(base_path, "red_meats.jpg"),
        "poultry": os.path.join(base_path, "poultry.jpg"),
        "chicken": os.path.join(base_path, "chicken.jpg"),
        "eggs": os.path.join(base_path, "eggs.jpg"),
        "dairy_products": os.path.join(base_path, "dairy_products.jpg"),
        "fish": os.path.join(base_path, "fish.jpg"),
        "legumes": os.path.join(base_path, "legumes.jpg"),
        "nuts": os.path.join(base_path, "nuts.jpg"),
        "tofu": os.path.join(base_path, "tofu.jpg"),
        "low-fat_dairy_products": os.path.join(base_path, "low-fat_dairy_products.jpg"),
        "cheese_sandwich": os.path.join(base_path, "cheese_sandwich.jpg"),
        "baru_nuts": os.path.join(base_path, "baru_nuts.jpg"),
        "beech_nuts": os.path.join(base_path, "beech_nuts.jpg"),
        "squash_seeds": os.path.join(base_path, "squash_seeds.jpg"),
        "mixed_teff": os.path.join(base_path, "mixed_teff.jpg"),
        "peanut_butter": os.path.join(base_path, "peanut_butter.jpg"),
        "jelly_sandwich": os.path.join(base_path, "jelly_sandwich.jpg"),
        "black_walnut": os.path.join(base_path, "black_walnut.jpg"),
        "hemp_seeds": os.path.join(base_path, "hemp_seeds.jpg"),
        "cheese": os.path.join(base_path, "cheese.jpg"),
        "cottage_cheese": os.path.join(base_path, "cottage_cheese.jpg"), # Typo fix
        "skim_milk": os.path.join(base_path, "skim_milk.jpg"),
        "low_fat_milk": os.path.join(base_path, "low_fat_milk.jpg"), # Typo fix

        # Juice
        "fruit_juice": os.path.join(base_path, "fruit_juice.jpg"),
        "apple_juice": os.path.join(base_path, "apple_juice.jpg"),
        "mango_juice": os.path.join(base_path, "mango_juice.jpg"),
        "carrot_juice": os.path.join(base_path, "carrot_juice.jpg"),
        "watermelon_juice": os.path.join(base_path, "watermelon_juice.jpg"),
        "beetroot_juice": os.path.join(base_path, "beetroot_juice.jpg"),
        "aloe_vera_juice": os.path.join(base_path, "aloe_vera_juice.jpg"),
        "cold-pressed_juice": os.path.join(base_path, "cold-pressed_juice.jpg"),
        "green_juice": os.path.join(base_path, "green_juice.jpg"),
        "kale_juice": os.path.join(base_path, "kale_juice.jpg"), # Placeholder, gak ada di list
        "spinach_juice": os.path.join(base_path, "spinach_juice.jpg"), # Placeholder
        "cucumber_juice": os.path.join(base_path, "cucumber_juice.jpg"), # Placeholder
        "celery_juice": os.path.join(base_path, "celery_juice.jpg"), # Placeholder
    }