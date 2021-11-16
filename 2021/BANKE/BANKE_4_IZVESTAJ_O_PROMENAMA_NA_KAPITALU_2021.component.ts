import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../../obrazac";
import { BackendServiceService } from "../../../backend-service.service";

@Component({
  selector: 'BANKE_4_IZVESTAJ_O_PROMENAMA_NA_KAPITALU_2021',
  templateUrl: 'BANKE_4_IZVESTAJ_O_PROMENAMA_NA_KAPITALU_2021.component.html',
})
export class BANKE_4_IZVESTAJ_O_PROMENAMA_NA_KAPITALU_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
