# Fitness Tracker - Calorie and Protein Counter

A command-line application to track your daily calorie and protein intake.

## Features

- Track food items with calorie and protein information
- Automatic nutritional information lookup
- Local database storage
- View all tracked items
- Daily statistics
- Handle multiple search results
- Error handling for invalid inputs

## Installation

1. Ensure you have Python 3.6+ installed
2. No additional dependencies required (uses Python standard library)

## Usage

### Track a food item

```bash
python fitness_tracker.py chicken breast
```

If multiple results are found, you'll be prompted to select one:
```
Found 2 results. Please select one:
1. Chicken Breast (100g, grilled) - 165 kcal, 31g protein
2. Chicken Breast (100g, fried) - 220 kcal, 28g protein

Enter selection (1-2): 1
```

### View all tracked items

```bash
python fitness_tracker.py --list
```

### View daily statistics

```bash
python fitness_tracker.py --stats
```

## Data Storage

All data is stored in a local SQLite database located at `data/fitness_tracker.db`.

## Supported Foods (Mock Data)

Currently using mock data for the following foods:
- Chicken breast
- Rice (white and brown)
- Eggs
- Apple
- Banana
- Salmon
- Broccoli
- Pasta
- Beef
- Milk

## Error Handling

The application handles:
- Invalid user inputs (empty food names, invalid selections)
- API failures (graceful error messages)
- Multiple search results (user selection)
- Database errors

## Future Enhancements

- Integration with real nutrition API (e.g., USDA FoodData Central, Nutritionix)
- Support for custom serving sizes
- Weekly/monthly statistics
- Export data to CSV
- Calorie and protein goals
