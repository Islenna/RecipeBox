import { Component } from '@angular/core';

@Component({
  selector: 'app-recipe-display',
  templateUrl: './recipe-display.component.html',
  styleUrls: ['./recipe-display.component.sass'],
  
})

export class RecipeDisplayComponent {
  
  toggleCompletion(event: any) {
    const target = event.target.closest('li');
    if (target) {
        target.classList.toggle('completed');
    }
}

}
