import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../../obrazac";
import { BackendServiceService } from "../../../backend-service.service";

@Component({
  selector: 'DPL_0_BILANS_STANJA_skraceni_obim_2021',
  templateUrl: 'DPL_0_BILANS_STANJA_skraceni_obim_2021.component.html',
})
export class DPL_0_BILANS_STANJA_skraceni_obim_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
