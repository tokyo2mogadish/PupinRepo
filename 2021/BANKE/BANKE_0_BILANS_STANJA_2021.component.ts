import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../../obrazac";
import { BackendServiceService } from "../../../backend-service.service";

@Component({
  selector: 'BANKE_0_BILANS_STANJA_2021',
  templateUrl: 'BANKE_0_BILANS_STANJA_2021.component.html',
})
export class BANKE_0_BILANS_STANJA_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
