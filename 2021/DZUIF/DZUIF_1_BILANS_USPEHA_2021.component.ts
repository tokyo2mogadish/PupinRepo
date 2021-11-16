import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../../obrazac";
import { BackendServiceService } from "../../../backend-service.service";

@Component({
  selector: 'DZUIF_1_BILANS_USPEHA_2021',
  templateUrl: 'DZUIF_1_BILANS_USPEHA_2021.component.html',
})
export class DZUIF_1_BILANS_USPEHA_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
