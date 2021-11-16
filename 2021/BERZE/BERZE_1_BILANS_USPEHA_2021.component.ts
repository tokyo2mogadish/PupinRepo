import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../../obrazac";
import { BackendServiceService } from "../../../backend-service.service";

@Component({
  selector: 'BERZE_1_BILANS_USPEHA_2021',
  templateUrl: 'BERZE_1_BILANS_USPEHA_2021.component.html',
})
export class BERZE_1_BILANS_USPEHA_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
