import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashComponent } from './dash/dash.component';
import { RecipeDisplayComponent } from './recipe-display/recipe-display.component';

const routes: Routes = [
  { path: '', component: DashComponent },
  { path: 'one', component: RecipeDisplayComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
