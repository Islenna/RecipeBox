import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class RecipeService {
  // URL to your backend API endpoint that gets all recipes.
  private apiUrl = 'http://localhost:3000/api/recipes'; // Change with your actual URL

  constructor(private http: HttpClient) { }

  getAllRecipes() {
    return this.http.get(this.apiUrl);
  }
}
