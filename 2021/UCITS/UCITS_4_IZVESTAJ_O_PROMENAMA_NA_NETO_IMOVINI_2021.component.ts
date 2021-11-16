import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../../obrazac";
import { BackendServiceService } from "../../../backend-service.service";

@Component({
  selector: 'UCITS_4_IZVESTAJ_O_PROMENAMA_NA_NETO_IMOVINI_2021',
  templateUrl: 'UCITS_4_IZVESTAJ_O_PROMENAMA_NA_NETO_IMOVINI_2021.component.html',
})
export class UCITS_4_IZVESTAJ_O_PROMENAMA_NA_NETO_IMOVINI_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
