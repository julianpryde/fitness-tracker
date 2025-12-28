#!/usr/bin/env python3
"""
Fitness Tracker - Command Line Calorie and Protein Counter
"""
import sys
import argparse
from datetime import datetime
from api_client import FoodAPIClient
from database import Database


def main():
    """Main entry point for the fitness tracker application."""
    parser = argparse.ArgumentParser(
        description='Track calories and protein intake from food items'
    )
    parser.add_argument(
        'food',
        nargs='*',
        help='Food item to track (e.g., "chicken breast")'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all tracked food items'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show daily statistics'
    )
    
    args = parser.parse_args()
    
    # Validate that either a food is provided or a flag is set
    if not args.food and not args.list and not args.stats:
        parser.error('Please provide a food item to track or use --list or --stats')
    
    if args.food and (args.list or args.stats):
        parser.error('Cannot specify food item with --list or --stats')
    
    # Initialize database
    db = Database()
    
    # Handle listing tracked items
    if args.list:
        entries = db.get_all_entries()
        if not entries:
            print("No food items tracked yet.")
            return
        
        print("\n=== Tracked Food Items ===")
        total_calories = 0
        total_protein = 0
        for entry in entries:
            print(f"{entry['timestamp']}: {entry['food_name']}")
            print(f"  Calories: {entry['calories']} kcal")
            print(f"  Protein: {entry['protein']} g")
            print()
            total_calories += entry['calories']
            total_protein += entry['protein']
        
        print(f"Total Calories: {total_calories} kcal")
        print(f"Total Protein: {total_protein} g")
        return
    
    # Handle statistics
    if args.stats:
        stats = db.get_daily_stats()
        if not stats:
            print("No statistics available yet.")
            return
        
        print("\n=== Daily Statistics ===")
        print(f"Total Calories: {stats['calories']} kcal")
        print(f"Total Protein: {stats['protein']} g")
        print(f"Items tracked: {stats['count']}")
        return
    
    # Track new food item
    if args.food:
        food_name = ' '.join(args.food)
        
        # Validate input
        if not food_name.strip():
            print("Error: Food name cannot be empty.", file=sys.stderr)
            sys.exit(1)
        
        print(f"Looking up nutritional information for: {food_name}")
        
        # Initialize API client
        api_client = FoodAPIClient()
        
        try:
            # Fetch nutritional data
            results = api_client.search_food(food_name)
            
            if not results:
                print(f"No nutritional information found for '{food_name}'.", file=sys.stderr)
                sys.exit(1)
            
            # Handle multiple results
            if len(results) > 1:
                print(f"\nFound {len(results)} results. Please select one:")
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result['name']} - {result['calories']} kcal, {result['protein']}g protein")
                
                while True:
                    try:
                        choice = input("\nEnter selection (1-{}): ".format(len(results)))
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(results):
                            selected = results[choice_idx]
                            break
                        else:
                            print("Invalid selection. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                    except KeyboardInterrupt:
                        print("\nCancelled.")
                        sys.exit(0)
            else:
                selected = results[0]
            
            # Store in database
            db.add_entry(
                food_name=selected['name'],
                calories=selected['calories'],
                protein=selected['protein']
            )
            
            print("\n=== Food Item Tracked ===")
            print(f"Food: {selected['name']}")
            print(f"Calories: {selected['calories']} kcal")
            print(f"Protein: {selected['protein']} g")
            print(f"Tracked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
