import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RecipeFormComponent } from './recipe-form/recipe-form.component';
import { RecipeDisplayComponent } from './recipe-display/recipe-display.component';
import { RecipeListComponent } from './recipe-list/recipe-list.component';
import { ModalComponent } from './modal/modal.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DashComponent } from './dash/dash.component';
import { NavbarComponent } from './navbar/navbar.component';

@NgModule({
  declarations: [
    AppComponent,
    RecipeFormComponent,
    RecipeDisplayComponent,
    RecipeListComponent,
    ModalComponent,
    DashComponent,
    NavbarComponent
    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
