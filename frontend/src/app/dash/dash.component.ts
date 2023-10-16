import { Component } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'app-chest',
  templateUrl: './dash.component.html',
  styleUrls: ['./dash.component.sass'],
  animations: [
    trigger('swingUp', [
      state('closed', style({
        transform: 'rotateX(0)'
      })),
      state('open', style({
        transform: 'rotateX(90deg)'
      })),
      transition('closed <=> open', [
        animate('2s')
      ]),
    ]),
    trigger('revealContents', [
      state('hidden', style({
        opacity: 0,
      })),
      state('visible', style({
        opacity: 1,
      })),
      transition('hidden <=> visible', [
        animate('2s')
      ]),
    ])
  ]
})
export class DashComponent {
  isLidOpen = false;
  areContentsVisible = false;

  toggleChest(): void {
    this.isLidOpen = !this.isLidOpen;
    this.areContentsVisible = !this.areContentsVisible;
  }
}
